"""One bounded, non-overwriting original-media custody attempt on macOS."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import plistlib
import shutil
import signal
import stat
import subprocess
import sys
import time
import uuid

ADMISSION = Path('/Users/4jp/Workspace/limen/scripts/host-work-admission.py')
OWNER = 'codex-ace-original-media-20261012'
RESERVE = 20 * 1024**3
VOLUMES = {
    'Ingress': '8E4C5386-7281-4E65-BC65-363C08FAAE50',
    'Archive4T': '45C8AA30-307B-41E2-908D-5112E93B4AF5',
    'T7Recovery': '0287E02B-989A-419B-A7CA-B4BCE4ECA1FF',
}


def command(args, timeout=30):
    return subprocess.check_output(args, timeout=timeout)


def identity(path):
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise RuntimeError('Source is not a regular file')
    return [s.st_size, s.st_mtime_ns, s.st_ino, s.st_dev]


def metadata(path):
    s = path.stat()
    names = command(['xattr', str(path)]).decode().splitlines()
    attrs = {n: command(['xattr', '-px', n, str(path)]).decode().split()
             for n in names}
    acl = command(['ls', '-lde', str(path)]).decode().splitlines()[1:]
    return {'mode': stat.S_IMODE(s.st_mode), 'mtime_ns': s.st_mtime_ns,
            'flags': s.st_flags, 'uid': s.st_uid, 'gid': s.st_gid,
            'xattrs': attrs, 'acl': acl}


def verified_entry_matches(path, entry, stage):
    """Reuse only a receipt whose verified object and metadata still match."""
    return (entry.get(stage + '_verified') is True
            and identity(path) == entry.get(stage + '_identity')
            and metadata(path) == entry['metadata'])


def destination_parent(path, volume):
    if not path.is_relative_to(volume) or path.resolve() != path:
        raise RuntimeError('destination escapes verified volume or traverses a symlink')
    path.parent.mkdir(mode=0o700, exist_ok=True)


def release_lease(lease):
    released = subprocess.run([sys.executable, str(ADMISSION), 'release',
        '--lease-id', lease['lease_id'], '--owner', OWNER, '--pid', str(os.getpid())],
        capture_output=True, timeout=30)
    result = json.loads(released.stdout)
    if released.returncode != 0 or result.get('allowed') is not True:
        raise RuntimeError('lease release rejected')
    return result


def partial_path(destination_root):
    parent = destination_root / '.custody-partials'
    parent.mkdir(mode=0o700, exist_ok=True)
    if parent.is_symlink():
        raise RuntimeError('linked partial root')
    return parent / uuid.uuid4().hex


def validate_device_separation(source, destination):
    src_p = Path(source)
    dst_p = Path(destination)
    while not src_p.exists() and src_p != src_p.parent:
        src_p = src_p.parent
    while not dst_p.exists() and dst_p != dst_p.parent:
        dst_p = dst_p.parent
    if not src_p.exists() or not dst_p.exists():
        raise RuntimeError('Source or destination mount point unavailable')
    if src_p.stat().st_dev == dst_p.stat().st_dev:
        raise RuntimeError(f'Source and destination are on the same physical device (st_dev={src_p.stat().st_dev})')


class PhaseDeadlineTracker:
    def __init__(self, wall_budget_s, verify_budget_s):
        self.wall_budget_s = float(wall_budget_s)
        self.verify_budget_s = float(verify_budget_s)
        self.started_at = time.monotonic()
        self.verification_seconds = 0.0
        self._active_verification_start = None

    @property
    def wall_elapsed(self):
        return time.monotonic() - self.started_at

    @property
    def current_verification_seconds(self):
        extra = 0.0
        if self._active_verification_start is not None:
            extra = time.monotonic() - self._active_verification_start
        return self.verification_seconds + extra

    def check_wall(self):
        if self.wall_elapsed >= self.wall_budget_s:
            raise TimeoutError('attempt wall deadline')

    def check_verify(self):
        if self.current_verification_seconds >= self.verify_budget_s:
            raise TimeoutError('verification time exhausted')

    def guard(self):
        self.check_wall()
        self.check_verify()

    def start_verification(self):
        self.check_wall()
        self.check_verify()
        if self._active_verification_start is None:
            self._active_verification_start = time.monotonic()

    def stop_verification(self):
        if self._active_verification_start is not None:
            self.verification_seconds += (time.monotonic() - self._active_verification_start)
            self._active_verification_start = None

    def measuring_verification(self):
        class _MeasureScope:
            def __init__(self, tracker):
                self.tracker = tracker
            def __enter__(self):
                self.tracker.start_verification()
                return self.tracker
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.tracker.stop_verification()
        return _MeasureScope(self)


def enumerate_source(source, roots):
    files, directories = {}, set()
    for root in roots:
        root_path = Path(root)
        if root_path.is_absolute() or '..' in root_path.parts or root in ('.', '', '.custody-partials'):
            raise RuntimeError('Path escape detected or unsafe root')
        start = source / root_path
        curr = start
        while curr != source and curr != curr.parent:
            if curr.is_symlink():
                raise RuntimeError('Unexpected source symlink in path')
            curr = curr.parent
        if not start.exists():
            raise RuntimeError('Source root unavailable or linked')
        if start.is_dir():
            rel_dir = str(root_path)
            if rel_dir in directories or rel_dir in files:
                raise RuntimeError(f'Duplicate destination directory: {rel_dir}')
            directories.add(rel_dir)
            for current, dirs, names in os.walk(start, followlinks=False,
                                                onerror=lambda e: (_ for _ in ()).throw(e)):
                for name in dirs:
                    p = Path(current) / name
                    if p.is_symlink():
                        raise RuntimeError('Unexpected source directory symlink')
                    d_rel = str(p.relative_to(source))
                    if d_rel in files:
                        raise RuntimeError(f'Duplicate destination: {d_rel}')
                    directories.add(d_rel)
                for name in names:
                    p = Path(current) / name
                    if p.is_symlink():
                        raise RuntimeError('Unexpected source symlink')
                    f_rel = str(p.relative_to(source))
                    if f_rel in files or f_rel in directories:
                        raise RuntimeError(f'Duplicate destination file: {f_rel}')
                    files[f_rel] = identity(p)
        elif start.is_file():
            s = start.lstat()
            if not stat.S_ISREG(s.st_mode):
                raise RuntimeError('Source is not a regular file')
            f_rel = str(root_path)
            if f_rel in files or f_rel in directories:
                raise RuntimeError(f'Duplicate destination file: {f_rel}')
            files[f_rel] = identity(start)
            for parent in root_path.parents:
                if str(parent) != '.':
                    directories.add(str(parent))
        else:
            raise RuntimeError('Source root is not a regular file or directory')
    return files, directories


def run(args):
    os.umask(0o077)
    os.nice(10)
    args.wall_budget_s = getattr(args, 'wall_budget_s', args.wall_seconds)
    args.verify_budget_s = getattr(args, 'verify_budget_s', args.verification_seconds)
    tracker = PhaseDeadlineTracker(args.wall_budget_s, args.verify_budget_s)
    private = (Path(args.resume) if args.resume else
               Path(args.staging) / ('original-media-' + uuid.uuid4().hex[:12]))
    if not args.resume:
        private.mkdir(mode=0o700)
    state = {'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'prior_agent_seconds': args.prior_seconds,
             'wall_limit_seconds': args.wall_seconds,
             'wall_budget_s': args.wall_seconds,
             'verification_limit_seconds': args.verification_seconds,
             'verify_budget_s': args.verification_seconds,
             'verification_seconds': 0.0, 'records': [], 'outcome': 'preflight',
             'originals_preserved': True, 'checkout_disposition': 'retained'}
    attempt_id = uuid.uuid4().hex[:12]
    if args.resume:
        previous = json.loads((private / 'receipt.json').read_text())
        consumed = previous['prior_agent_seconds'] + previous['elapsed_seconds']
        if args.prior_seconds < consumed:
            raise RuntimeError('resume understates cumulative usage')
        state['records'] = previous['records']
        for key in ['custody_path', 'restore_path', 'inventory_sha256']:
            if key in previous:
                state[key] = previous[key]
    lease = None
    last_refresh = tracker.started_at

    def save():
        state['elapsed_seconds'] = tracker.wall_elapsed
        state['verification_seconds'] = tracker.current_verification_seconds
        tmp = private / 'receipt.next.json'
        with tmp.open('w') as f:
            json.dump(state, f, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, private / 'receipt.json')

    def guard():
        nonlocal last_refresh
        tracker.guard()
        state['verification_seconds'] = tracker.current_verification_seconds
        if lease and time.monotonic() - last_refresh > 60:
            result = json.loads(command([sys.executable, str(ADMISSION), 'refresh',
                '--lease-id', lease['lease_id'], '--owner', OWNER,
                '--pid', str(os.getpid()), '--ttl-seconds', '1800']))
            if not result['allowed']:
                raise RuntimeError('lease refresh refused')
            last_refresh = time.monotonic()

    def checked_metadata(path):
        guard()
        with tracker.measuring_verification():
            result = metadata(path)
        guard()
        return result

    def digest(path):
        h = hashlib.sha256()
        with tracker.measuring_verification():
            before = identity(path)
            with path.open('rb') as f:
                while True:
                    guard()
                    chunk = f.read(4 * 1024**2)
                    if not chunk:
                        break
                    h.update(chunk)
            if identity(path) != before:
                raise RuntimeError('file changed while hashing')
            return h.hexdigest()

    def transfer(src, dst, expected, expected_metadata):
        guard()
        if dst.exists():
            if digest(dst) == expected and checked_metadata(dst) == expected_metadata:
                return  # Recover promotion interrupted before its receipt checkpoint.
            raise FileExistsError('destination exists with unverified content')
        if shutil.disk_usage(dst.parent).free < src.stat().st_size + RESERVE:
            raise RuntimeError('destination reserve unavailable')
        destination_root = next(Path(state[k]) for k in ('custody_path', 'restore_path')
                                if dst.is_relative_to(Path(state[k])))
        partial = partial_path(destination_root)
        # A fresh exclusive placeholder ensures this invocation owns the temporary name.
        with partial.open('xb'):
            pass
        remaining_wall = max(0.1, tracker.wall_budget_s - tracker.wall_elapsed)
        subprocess.run(['ditto', '--rsrc', '--extattr', '--acl', str(src), str(partial)],
                       check=True, timeout=min(300, remaining_wall))
        guard()
        if shutil.disk_usage(dst.parent).free < RESERVE:
            raise RuntimeError('destination reserve consumed by all-fork copy')
        with partial.open('rb') as f:
            os.fsync(f.fileno())
        if digest(partial) != expected or checked_metadata(partial) != expected_metadata:
            raise RuntimeError('copy readback or metadata mismatch; partial retained')
        # link is exclusive and refuses an existing final name (same filesystem).
        os.link(partial, dst)
        partial.unlink()  # Only the verified temporary alias; original bytes remain at dst.

    def alarm_handler(_signum, _frame):
        raise TimeoutError('hard process deadline')

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.signal(signal.SIGTERM, alarm_handler)
    signal.alarm(args.wall_seconds)
    try:
        invpath = Path(args.inventory)
        invbytes = invpath.read_bytes()
        if hashlib.sha256(invbytes).hexdigest() != args.inventory_sha256:
            raise RuntimeError('inventory digest mismatch')
        if state.get('inventory_sha256', args.inventory_sha256) != args.inventory_sha256:
            raise RuntimeError('resume inventory changed')
        state['inventory_sha256'] = args.inventory_sha256
        inventory = json.loads(invbytes)
        if any(Path(p).is_absolute() or '..' in Path(p).parts or p in ('.', '', '.custody-partials')
               for p in inventory['roots']):
            raise RuntimeError('unsafe content root')
        expected = {r['path']: [r['bytes'], r['mtime_ns'], r['inode'], r['device']]
                    for r in inventory['files']}
        if any(Path(p).is_absolute() or '..' in Path(p).parts for p in expected):
            raise RuntimeError('unsafe source path')
        if len({p.casefold() for p in expected}) != len(expected):
            raise RuntimeError('case-insensitive filename collision')
        source = Path('/Volumes/Ingress')
        actual, directories = enumerate_source(source, inventory['roots'])
        if actual != expected:
            raise RuntimeError('source differs from frozen inventory')
        directory_metadata = {}
        for rel in directories:
            m = checked_metadata(source / rel)
            if m['acl'] or m['xattrs'] or m['flags']:
                raise RuntimeError('directory metadata requires metadata-only restoration')
            directory_metadata[rel] = m
        disks = {}
        for name, volume_uuid in VOLUMES.items():
            info = plistlib.loads(command(['diskutil', 'info', '-plist', '/Volumes/' + name]))
            if info['VolumeUUID'] != volume_uuid:
                raise RuntimeError('volume identity mismatch')
            disks[name] = {'uuid': volume_uuid, 'parent': info['ParentWholeDisk'],
                           'free_bytes': shutil.disk_usage('/Volumes/' + name).free}
        state['disks'] = disks
        if disks['Ingress']['parent'] == disks['T7Recovery']['parent']:
            raise RuntimeError('custody device is not independent')
        if disks['Archive4T']['parent'] == disks['T7Recovery']['parent']:
            raise RuntimeError('restore device is not independent of custody')
        validate_device_separation(source, Path('/Volumes/T7Recovery'))
        validate_device_separation(Path('/Volumes/T7Recovery'), Path('/Volumes/Archive4T'))
        previous_by_path = {r['path']: r for r in state['records']}
        total = sum(v[0] for v in expected.values())
        for name in ['T7Recovery', 'Archive4T']:
            stage = 'custody' if name == 'T7Recovery' else 'restore'
            remaining = sum(v[0] for p, v in expected.items()
                            if not previous_by_path.get(p, {}).get(stage + '_verified'))
            if disks[name]['free_bytes'] < remaining + RESERVE:
                raise RuntimeError('full destination capacity unavailable')
        opened = subprocess.run(['lsof', '-n', '-P', '+f', '--', str(source)],
                                capture_output=True, timeout=30)
        if opened.returncode != 1 or opened.stdout:
            raise RuntimeError('source has open handles or open-handle probe failed')
        admission = subprocess.run([sys.executable, str(ADMISSION), 'acquire',
            '--kind', 'heavy', '--owner', OWNER, '--surface', 'original-media-custody',
            '--pid', str(os.getpid()), '--ttl-seconds', '1800'],
            capture_output=True, timeout=30)
        state['admission'] = json.loads(admission.stdout)
        if admission.returncode != 0 or not state['admission']['allowed']:
            raise RuntimeError('host admission refused')
        lease = state['admission']['lease']
        custody_name = private.name
        custody = Path(state.get('custody_path', str(Path('/Volumes/T7Recovery/limen-custody') / custody_name)))
        restore = Path(state.get('restore_path', str(Path('/Volumes/Archive4T/limen-custody') / custody_name)))
        for p in [custody, restore]:
            volume = Path('/Volumes/T7Recovery' if p == custody else '/Volumes/Archive4T')
            destination_parent(p, volume)
            p.mkdir(mode=0o700, exist_ok=bool(args.resume))
            for rel in sorted(directories, key=lambda s: (s.count('/'), s)):
                (p / rel).mkdir(mode=0o700, exist_ok=bool(args.resume))
        state.update(custody_path=str(custody), restore_path=str(restore), outcome='hashing')
        save()
        print(json.dumps({'staging': str(private), 'phase': 'hashing', 'admitted': True}), flush=True)
        for rel in sorted(expected):
            guard()
            p = source / rel
            if identity(p) != expected[rel]:
                raise RuntimeError('source drift before hashing')
            r = previous_by_path.get(rel)
            if r is None:
                r = {'path': rel, 'bytes': expected[rel][0], 'metadata': checked_metadata(p),
                     'sha256': digest(p), 'hashed': True}
                state['records'].append(r)
                save()
            elif checked_metadata(p) != r['metadata']:
                raise RuntimeError('source metadata changed since checkpoint')
            for stage, src, dst in [('custody', p, custody / rel),
                                    ('restore', custody / rel, restore / rel)]:
                if r.get(stage + '_verified'):
                    if (not verified_entry_matches(dst, r, stage)
                            or digest(dst) != r['sha256']):
                        raise RuntimeError('verified destination changed since checkpoint')
                else:
                    transfer(src, dst, r['sha256'], r['metadata'])
                    r[stage + '_verified'] = True
                    r[stage + '_identity'] = identity(dst)
                    save()
            save()
            print(json.dumps({'hashed': len(state['records']),
                'restored': sum(e.get('restore_verified', False) for e in state['records']),
                'verified_bytes': sum(e['bytes'] for e in state['records'] if e.get('restore_verified')),
                'verification_seconds': round(state['verification_seconds'], 2)}), flush=True)
        for destination in [custody, restore]:
            # Apply and verify directory metadata only after children are complete.
            for rel in sorted(directories, key=lambda s: (-s.count('/'), s)):
                src, dst = source / rel, destination / rel
                # ditto directory copies could overwrite files; refuse nontrivial directory
                # metadata until a dedicated metadata-only method has been verified.
                m = checked_metadata(src)
                if m != directory_metadata[rel]:
                    raise RuntimeError('source directory metadata drift')
                if m['acl'] or m['xattrs'] or m['flags']:
                    raise RuntimeError('directory metadata requires metadata-only restoration')
                shutil.copystat(src, dst)
                if checked_metadata(dst) != m:
                    raise RuntimeError('directory metadata mismatch')
            found, found_dirs = enumerate_source(destination, inventory['roots'])
            if set(found) != set(expected) or found_dirs != directories:
                raise RuntimeError('destination membership mismatch')
            for r in state['records']:
                if (digest(destination / r['path']) != r['sha256']
                        or checked_metadata(destination / r['path']) != r['metadata']):
                    raise RuntimeError('destination changed at completion')
        final, final_dirs = enumerate_source(source, inventory['roots'])
        if final != expected or final_dirs != directories:
            raise RuntimeError('source drift at completion')
        for r in state['records']:
            if checked_metadata(source / r['path']) != r['metadata']:
                raise RuntimeError('source metadata drift at completion')
        guard()
        state['outcome'] = 'verified-complete'
    except Exception as exc:
        state['outcome'] = 'checkpoint-incomplete'
        state['reason'] = str(exc)
    finally:
        signal.alarm(0)
        if lease:
            try:
                state['release'] = release_lease(lease)
            except Exception as exc:
                state['release_error'] = str(exc)
                state['outcome'] = 'checkpoint-incomplete'
        save()
        with (private / ('attempt-' + attempt_id + '.json')).open('x') as f:
            json.dump(state, f, indent=2)
        for name in ['custody_path', 'restore_path']:
            if name in state:
                target = Path(state[name]) / ('custody-receipt-' + attempt_id + '.json')
                with target.open('x') as f:
                    json.dump(state, f, indent=2)
        print(json.dumps({'staging': str(private), 'outcome': state['outcome'],
                          'reason': state.get('reason'), 'hashed': len(state['records']),
                          'custody_verified': sum(r.get('custody_verified', False) for r in state['records']),
                          'restore_verified': sum(r.get('restore_verified', False) for r in state['records'])}), flush=True)
    return 0 if state['outcome'] == 'verified-complete' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', required=True)
    parser.add_argument('--inventory-sha256', required=True)
    parser.add_argument('--staging', required=True)
    parser.add_argument('--resume', help='Existing private receipt directory; preserves prior attempts')
    parser.add_argument('--prior-seconds', type=int, required=True)
    parser.add_argument('--wall-seconds', '--wall-budget-s', dest='wall_seconds', type=int, default=1500)
    parser.add_argument('--verification-seconds', '--verify-budget-s', dest='verification_seconds', type=int, default=540)
    args = parser.parse_args()
    if not (0 < args.wall_seconds <= 1800 and 0 < args.verification_seconds <= 600
            and 0 <= args.prior_seconds and args.prior_seconds + args.wall_seconds <= 7200):
        parser.error('finite attempt or cumulative budget exceeded')
    raise SystemExit(run(args))
