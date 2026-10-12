"""Local fixture checks; these do not establish physical custody."""
import importlib.util
from pathlib import Path
import subprocess
import shutil
import os
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('custody_danse',
    Path(__file__).parents[1] / 'custody_danse.py')
CUSTODY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CUSTODY)


class CustodyTests(unittest.TestCase):
    def test_links_are_recorded_without_following(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'external').symlink_to('/tmp', target_is_directory=True)
            files, directories = CUSTODY.census(root)
            self.assertEqual(set(files), {'external'})
            self.assertEqual(set(directories), {'.'})
            signature = CUSTODY.content_signature(root, (files, directories), lambda: None)
            self.assertEqual(signature['external']['target'], '/tmp')

    def test_special_nodes_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            os.mkfifo(root / 'fifo')
            with self.assertRaisesRegex(RuntimeError, 'special material'):
                CUSTODY.census(root)

    def test_private_parent_rejects_public_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'public'
            root.mkdir(mode=0o755)
            root.chmod(0o755)
            with self.assertRaisesRegex(RuntimeError, 'private'):
                CUSTODY.private_directory(root)

    def test_full_store_preserves_stash_reflog_and_local_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'source'
            root.mkdir()
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.DEVNULL)
            git('init', '-b', 'main')
            git('config', 'user.name', 'Custody Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('remote', 'add', 'origin', 'https://example.invalid/private.git')
            (root / 'file').write_text('base\n')
            (root / '.gitignore').write_text('ignored\n')
            git('add', 'file', '.gitignore')
            git('commit', '-m', 'fixture')
            git('branch', 'local-only')
            for value in ['first', 'second']:
                (root / 'file').write_text(value)
                git('stash', 'push', '-m', value)
            (root / 'ignored').write_bytes(b'private material\x00')
            before = CUSTODY.git_state(root)
            self.assertEqual(len(before['stash_entries'].splitlines()), 2)
            inventory = CUSTODY.census(root)
            signature = CUSTODY.content_signature(root, inventory, lambda: None)
            restored = Path(tmp) / 'restored'
            restored.mkdir()
            subprocess.run(['ditto', '--rsrc', '--extattr', '--acl', str(root), str(restored)], check=True)
            shutil.copystat(root, restored)
            restored_signature = CUSTODY.content_signature(restored, CUSTODY.census(restored),
                                                           lambda: None, durable=True)
            self.assertEqual([p for p in signature if signature[p] != restored_signature.get(p)], [])
            self.assertEqual(CUSTODY.git_state(restored), before)
            self.assertEqual(CUSTODY.git_state(root), before)
            self.assertEqual(CUSTODY.census(root), inventory)
            subprocess.run(['git', 'fsck', '--full', '--no-progress'], cwd=restored, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    unittest.main()
