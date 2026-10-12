import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'custody_original_media.py'
spec = importlib.util.spec_from_file_location('custody', SCRIPT)
custody = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custody)


class CustodyTests(unittest.TestCase):
    def test_retained_partials_do_not_enter_content_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'media').mkdir()
            custody.partial_path(root).write_bytes(b'interrupted payload')
            self.assertEqual(custody.enumerate_source(root, ['media']), ({}, {'media'}))

    def test_destination_rejects_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'actual').mkdir()
            (root / 'limen-custody').symlink_to(root / 'actual', target_is_directory=True)
            with self.assertRaisesRegex(RuntimeError, 'symlink'):
                custody.destination_parent(root / 'limen-custody' / 'attempt', root)

    def test_rejected_or_malformed_release_cannot_succeed(self):
        for code, output in [(1, b'{"allowed":true}'), (0, b'{"allowed":false}'), (0, b'invalid')]:
            with patch.object(custody.subprocess, 'run', return_value=subprocess.CompletedProcess([], code, output)):
                with self.assertRaises((RuntimeError, ValueError)):
                    custody.release_lease({'lease_id': 'fixture'})

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS xattrs and stat flags')
    def test_resume_refuses_replaced_or_changed_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'verified'
            path.write_bytes(b'original')
            entry = {'custody_verified': True,
                     'custody_identity': custody.identity(path),
                     'metadata': custody.metadata(path)}
            self.assertTrue(custody.verified_entry_matches(path, entry, 'custody'))
            path.write_bytes(b'changed payload')
            self.assertFalse(custody.verified_entry_matches(path, entry, 'custody'))

    def test_enumeration_refuses_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'media').mkdir()
            (root / 'media' / 'link').symlink_to('/tmp')
            with self.assertRaises(RuntimeError):
                custody.enumerate_source(root, ['media'])

    def test_budget_rejected_before_io(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--inventory', '/nonexistent',
            '--inventory-sha256', 'unused', '--staging', '/nonexistent',
            '--prior-seconds', '7100', '--wall-seconds', '200'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'cumulative budget exceeded', result.stderr)


if __name__ == '__main__':
    unittest.main()
