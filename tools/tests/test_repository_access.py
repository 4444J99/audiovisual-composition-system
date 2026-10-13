import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("access", Path(__file__).resolve().parents[1] / "verify_repository_access.py")
access = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(access)


class RepositoryAccessTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {"access": {"repository_id": 1413700288, "observed_visibility": "public"}}
        self.metadata = {"id": 1413700288, "visibility": "public", "private": False, "archived": False}

    def test_current_public_observation_passes(self):
        self.assertTrue(access.verify_access(self.manifest, self.metadata)["verified"])

    def test_rename_does_not_change_identity(self):
        self.metadata["full_name"] = "example/renamed-system"
        self.assertTrue(access.verify_access(self.manifest, self.metadata)["verified"])

    def test_replacement_and_unknown_visibility_fail_closed(self):
        for change in ({"id": 1}, {"id": True}, {"visibility": None}, {"visibility": "unknown"}, {"visibility": "private"}, {"private": True}, {"archived": True}, {"archived": None}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                access.verify_access(self.manifest, {**self.metadata, **change})


if __name__ == "__main__":
    unittest.main()
