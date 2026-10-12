"""Bounded private custody of a standalone Danse checkout, including its Git store.

Never changes the source or publishes its contents. A denied attempt retains its
private census and emits an explicitly incomplete, redacted receipt.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True  # Importing the native helper must not write into the source.

ADMISSION = Path('/Users/4jp/Workspace/limen/scripts/host-work-admission.py')
STAGING = Path('/Users/4jp/Workspace/limen/.limen-private/custody-staging')
OWNER = 'codex-danse-private-custody'
RESERVE = 20 * 1024**3


def command(args, cwd=None, timeout=30):
    return subprocess.check_output(args, cwd=cwd, timeout=timeout,
                                   env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})


def git_state(root):
    def git(*args):
        return command(['git', *args], cwd=root).decode().strip()
    return {'head': git('rev-parse', 'HEAD'),
            'branch': git('symbolic-ref', 'HEAD'),
            'refs': git('for-each-ref', '--format=%(refname) %(objectname)'),
            'stash_entries': git('reflog', 'show', '--format=%H', 'refs/stash'),
            'tracked_status': git('status', '--porcelain', '--untracked-files=no'),
            'remotes': git('config', '--get-regexp', '^remote\\..*\\.(url|pushurl)$')}


def census(root):
    """Record literal links without following them; reject special nodes."""
    files, directories = {}, {}
    def inspect(path, destination):
        s = path.lstat()
        if not (stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode) or stat.S_ISLNK(s.st_mode)):
            raise RuntimeError('special material requires separate custody')
        destination[str(path.relative_to(root))] = [s.st_size, s.st_mtime_ns,
            stat.S_IMODE(s.st_mode), s.st_ino, s.st_dev, s.st_flags, stat.S_IFMT(s.st_mode)]
    inspect(root, directories)
    for current, dirs, names in os.walk(root, followlinks=False,
            onerror=lambda e: (_ for _ in ()).throw(e)):
        for name in list(dirs):
            path = Path(current) / name
            if path.is_symlink():
                inspect(path, files)
                dirs.remove(name)
            else:
                inspect(path, directories)
        for name in names:
            inspect(Path(current) / name, files)
    return files, directories


def content_signature(root, inventory, guard, durable=False):
    result = {}
    files, directories = inventory
    for rel, expected in {**directories, **files}.items():
        guard()
        path = root / rel
        s = path.lstat()
        # Directory sizes and inode/device identifiers differ between filesystems.
        entry = {'mode': stat.S_IMODE(s.st_mode), 'mtime_ns': s.st_mtime_ns,
                 'flags': s.st_flags, 'uid': s.st_uid, 'gid': s.st_gid}
        if path.is_symlink():
            entry.update(kind='symlink', target=os.readlink(path))
            result[rel] = entry
            continue
        names = command(['xattr', str(path)]).decode().splitlines()
        attrs = {name: hashlib.sha256(command(['xattr', '-px', name, str(path)])).hexdigest()
                 for name in names}
        entry['xattrs'] = attrs
        entry['acl'] = command(['ls', '-lde', str(path)]).decode().splitlines()[1:]
        if rel in files:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                if durable:
                    os.fsync(stream.fileno())
                while chunk := stream.read(4 * 1024**2):
                    guard()
                    digest.update(chunk)
            entry.update(bytes=s.st_size, sha256=digest.hexdigest())
        result[rel] = entry
    return result


def private_directory(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    s = path.lstat()
    if path.is_symlink() or not path.is_dir() or s.st_uid != os.getuid() or s.st_mode & 0o077:
        raise RuntimeError('custody parent must be owned, private and unlinked')


def run(args):
    os.umask(0o077)
    os.nice(10)
    started = time.monotonic()
    private_directory(STAGING)
    run_id = 'danse-' + uuid.uuid4().hex
    private = STAGING / run_id
    private.mkdir(mode=0o700)
    state = {'schema': 'danse.private-custody-attempt.v1', 'run_id': run_id,
             'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'outcome': 'preflight', 'copies_verified': 0, 'clean_restore_verified': False,
             'source_preserved': None, 'checkout_disposition': 'retained',
             'scope': 'one current standalone checkout, complete Git store and working tree',
             'wall_limit_seconds': args.wall_seconds, 'verification_limit_seconds': 600}
    lease = None
    before = None
    inventory = None
    last_refresh = started
    verification_started = None

    def save():
        state['elapsed_seconds'] = round(time.monotonic() - started, 3)
        (private / 'receipt.json').write_text(json.dumps(state, indent=2) + '\n')

    def guard():
        nonlocal last_refresh
        now = time.monotonic()
        if now - started >= args.wall_seconds:
            raise TimeoutError('attempt deadline')
        if verification_started and now - verification_started >= 600:
            raise TimeoutError('verification deadline')
        if lease and now - last_refresh >= 60:
            refreshed = json.loads(command([sys.executable, str(ADMISSION), 'refresh',
                '--lease-id', lease['lease_id'], '--owner', OWNER, '--pid', str(os.getpid()),
                '--ttl-seconds', str(args.wall_seconds)]))
            if not refreshed['allowed']:
                raise RuntimeError('lease refresh refused')
            last_refresh = now

    def alarm_handler(_signum, _frame):
        raise TimeoutError('hard process deadline')

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(args.wall_seconds)
    try:
        source = Path(args.source).absolute()
        if (source.is_symlink() or source.resolve() != source or not (source / '.git').is_dir()
                or (source / '.git').is_symlink()):
            raise RuntimeError('source must be a standalone, unlinked checkout')
        before = git_state(source)
        inventory = census(source)
        common = command(['git', 'rev-parse', '--git-common-dir'], source).decode().strip()
        if (source / common).resolve() != source / '.git':
            raise RuntimeError('external common Git store')
        if any(v[-1] == stat.S_IFLNK for p, v in inventory[0].items() if p.startswith('.git/')):
            raise RuntimeError('linked Git-store material requires separate custody')
        if before['tracked_status']:
            raise RuntimeError('tracked source is dirty')
        if command(['git', 'rev-parse', '--is-shallow-repository'], source).strip() != b'false':
            raise RuntimeError('shallow Git store')
        if (source / '.git/objects/info/alternates').exists() or (source / '.gitmodules').exists():
            raise RuntimeError('external Git objects or submodules need separate custody')
        worktree = subprocess.run(['git', 'config', '--get', 'core.worktree'], cwd=source,
                                  capture_output=True, timeout=30)
        if worktree.returncode not in (0, 1) or worktree.stdout.strip():
            raise RuntimeError('external Git worktree configuration')
        if any(Path(p).name.endswith('.lock') for p in inventory[0] if p.startswith('.git/')):
            raise RuntimeError('Git store has an active or retained lock')
        ignored = command(['git', 'ls-files', '--others', '--ignored', '--exclude-standard', '-z'], source)
        names = [os.fsdecode(p) for p in ignored.split(b'\0') if p]
        if any(p not in inventory[0] for p in names):
            raise RuntimeError('ignored inventory contains unavailable material')
        state.update(source_head=before['head'], ref_count=len(before['refs'].splitlines()),
            stash_entry_count=len(before['stash_entries'].splitlines()),
            ignored_file_count=len(names), ignored_bytes=sum(inventory[0][p][0] for p in names),
            total_file_count=len(inventory[0]), total_bytes=sum(v[0] for v in inventory[0].values()))
        (private / 'preflight.json').write_text(json.dumps({'source': str(source),
            'git': before, 'files': inventory[0], 'directories': inventory[1], 'ignored': names}, indent=2))
        helper = source / 'scripts/private_custody.py'
        state['native_medium_helper_sha256'] = hashlib.sha256(helper.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location('danse_native_custody', helper)
        native = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = native
        spec.loader.exec_module(native)
        roots = [Path('/Volumes/T7Recovery'), Path('/Volumes/Archive4T')]
        medium_ids = native.ensure_independent(*roots)
        state['independent_media_sha256'] = list(medium_ids)
        for root in [*roots, STAGING]:
            if shutil.disk_usage(root).free < state['total_bytes'] + RESERVE:
                raise RuntimeError('destination reserve unavailable')
        state['capacity_and_medium_preflight'] = True
        decision = subprocess.run([sys.executable, str(ADMISSION), 'acquire', '--kind', 'heavy',
            '--owner', OWNER, '--surface', 'danse-private-custody', '--pid', str(os.getpid()),
            '--ttl-seconds', str(args.wall_seconds)], capture_output=True, timeout=30)
        state['admission'] = json.loads(decision.stdout)
        if decision.returncode != 0 or not state['admission']['allowed']:
            state['outcome'] = 'blocked-admission'
            raise RuntimeError('host admission refused; no payload hashed or copied')
        lease = state['admission']['lease']
        if args.preflight_only:
            state['outcome'] = 'preflight-only'
            return 1  # Never promote admission/preflight into successful custody.
        verification_started = time.monotonic()
        signature = content_signature(source, inventory, guard)
        if census(source) != inventory or git_state(source) != before:
            raise RuntimeError('source changed during hashing; no copy started')
        (private / 'checksums-and-metadata.json').write_text(json.dumps(signature, indent=2))
        state['inventory_sha256'] = hashlib.sha256(json.dumps(signature, sort_keys=True).encode()).hexdigest()
        previous = source
        for index, root in enumerate([*roots, private]):
            guard()
            parent = root / 'limen-custody' if index < 2 else root
            private_directory(parent)
            target = parent / run_id if index < 2 else parent / 'restore'
            target.mkdir(mode=0o700)  # Exclusive name, never overwrite a retained attempt.
            subprocess.run(['ditto', '--rsrc', '--extattr', '--acl', str(previous), str(target)],
                check=True, timeout=max(1, args.wall_seconds - (time.monotonic() - started)))
            # ditto into an exclusively precreated directory leaves its root mtime.
            shutil.copystat(previous, target)
            restored_inventory = census(target)
            if set(restored_inventory[0]) != set(inventory[0]) or set(restored_inventory[1]) != set(inventory[1]):
                raise RuntimeError('copy membership mismatch; partial retained')
            if content_signature(target, restored_inventory, guard, durable=True) != signature:
                raise RuntimeError('copy hash or metadata mismatch; partial retained')
            state.setdefault('private_copy_paths', []).append(str(target))
            if index < 2:
                state['copies_verified'] += 1
            else:
                if git_state(target) != before:
                    raise RuntimeError('restored Git state mismatch')
                command(['git', 'fsck', '--full', '--no-progress'], target, timeout=120)
                state['clean_restore_verified'] = True
            save()
            previous = target
            if census(source) != inventory or git_state(source) != before:
                raise RuntimeError('source changed during copy; partials retained')
        guard()
        if census(source) != inventory or git_state(source) != before:
            raise RuntimeError('source changed during custody')
        state['outcome'] = 'verified-complete'
    except Exception as exc:
        if state['outcome'] != 'blocked-admission':
            state['outcome'] = 'checkpoint-incomplete'
        # Exception text may contain private paths; retain details privately only.
        state['private_failure'] = str(exc)
        state['failure_class'] = type(exc).__name__
    finally:
        signal.alarm(0)
        if before is not None:
            try:
                state['git_state_preserved'] = git_state(source) == before
                state['source_preserved'] = (state['git_state_preserved'] and census(source) == inventory
                                             if inventory is not None else None)
            except Exception:
                state['source_preserved'] = False
        if not state['source_preserved'] and state['outcome'] == 'verified-complete':
            state['outcome'] = 'checkpoint-incomplete'
        if lease:
            released = subprocess.run([sys.executable, str(ADMISSION), 'release',
                '--lease-id', lease['lease_id'], '--owner', OWNER, '--pid', str(os.getpid())],
                capture_output=True, timeout=30)
            state['lease_release'] = json.loads(released.stdout)
        save()
        public = {k: v for k, v in state.items() if not k.startswith('private_')}
        # Admission sensor data is numerical/process metadata, not source content.
        with Path(args.redacted_receipt).open('x') as stream:
            json.dump(public, stream, indent=2)
            stream.write('\n')
        print(json.dumps({'outcome': state['outcome'], 'private_receipt': str(private / 'receipt.json'),
                          'copies_verified': state['copies_verified'],
                          'clean_restore_verified': state['clean_restore_verified']}))
    return 0 if state['outcome'] == 'verified-complete' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--redacted-receipt', required=True)
    parser.add_argument('--wall-seconds', type=int, default=1200)
    parser.add_argument('--preflight-only', action='store_true',
                        help='record admission and inventory without hashing or copying payload')
    args = parser.parse_args()
    if not 0 < args.wall_seconds <= 1800:
        parser.error('wall deadline must be at most 1800 seconds')
    raise SystemExit(run(args))
