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

    def test_individual_file_enumeration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            f1 = root / 'sample.bin'
            f1.write_bytes(b'abc')
            (root / 'sub').mkdir()
            f2 = root / 'sub' / 'nested.bin'
            f2.write_bytes(b'defgh')

            files, dirs = custody.enumerate_source(root, ['sample.bin', 'sub/nested.bin'])
            self.assertEqual(set(files.keys()), {'sample.bin', 'sub/nested.bin'})
            self.assertEqual(dirs, {'sub'})
            self.assertEqual(files['sample.bin'][0], 3)
            self.assertEqual(files['sub/nested.bin'][0], 5)

            # Duplicate destination rejection
            with self.assertRaisesRegex(RuntimeError, '[Dd]uplicate'):
                custody.enumerate_source(root, ['sample.bin', 'sample.bin'])
            with self.assertRaisesRegex(RuntimeError, '[Dd]uplicate'):
                custody.enumerate_source(root, ['sub', 'sub/nested.bin'])

            # Path escape rejection
            with self.assertRaisesRegex(RuntimeError, 'escape|unsafe'):
                custody.enumerate_source(root, ['../outside.txt'])

            # Symlink refusal
            link = root / 'link.bin'
            link.symlink_to(f1)
            with self.assertRaisesRegex(RuntimeError, 'symlink|linked'):
                custody.enumerate_source(root, ['link.bin'])

    def test_same_device_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            src = root / 'source'
            dst = root / 'destination'
            src.mkdir()
            dst.mkdir()

            # Same filesystem has matching st_dev and must be rejected
            with self.assertRaisesRegex(RuntimeError, 'same physical device'):
                custody.validate_device_separation(src, dst)

            # Independent physical devices with differing st_dev must pass
            class MockStat:
                def __init__(self, dev):
                    self.st_dev = dev

            def fake_stat(path_obj):
                if path_obj == src:
                    return MockStat(1001)
                return MockStat(2002)

            with patch.object(Path, 'stat', fake_stat):
                # Should not raise
                custody.validate_device_separation(src, dst)

    def test_phase_deadline_enforcement(self):
        tracker = custody.PhaseDeadlineTracker(wall_budget_s=50, verify_budget_s=10)

        current_time = [100.0]
        with patch.object(custody.time, 'monotonic', side_effect=lambda: current_time[0]):
            tracker.started_at = 100.0

            # 1. Non-verification phase takes 30s wall time: does NOT consume verification budget
            current_time[0] = 130.0
            tracker.guard()  # Wall elapsed = 30s (< 50s), verify elapsed = 0s (< 10s)
            self.assertEqual(tracker.current_verification_seconds, 0.0)

            # 2. Wall budget exhaustion raises independently of verify budget
            current_time[0] = 151.0
            with self.assertRaisesRegex(TimeoutError, 'attempt wall deadline'):
                tracker.guard()

            # Reset tracker for verify budget testing
            tracker2 = custody.PhaseDeadlineTracker(wall_budget_s=1000, verify_budget_s=10)
            tracker2.started_at = 200.0
            current_time[0] = 200.0

            # Inside verification phase, advancing beyond verify_budget_s raises
            with tracker2.measuring_verification():
                current_time[0] = 211.0
                with self.assertRaisesRegex(TimeoutError, 'verification time exhausted'):
                    tracker2.guard()


if __name__ == '__main__':
    unittest.main()
