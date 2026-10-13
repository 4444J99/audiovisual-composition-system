import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("implementation", Path(__file__).resolve().parents[1] / "validate_implementation.py")
implementation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(implementation)


class ImplementationContractTests(unittest.TestCase):
    def setUp(self):
        self.data = {"schema_version": "1.0.0", "system_id": "audiovisual-composition-system", "repository": {"github_id": 1}, "software": {"id": "frame-compositor", "name": "Frame compositor", "responsibility": "Compose frames"}, **{kind: [] for kind in implementation.KINDS}}
        self.data["capabilities"] = [{"id": "frame-composition"}]
        self.data["modules"] = [{"id": "frames", "path": "frames.py", "capability_ids": ["frame-composition"], "interfaces": ["compose"]}]
        self.data["artworks"] = [{"id": "work-001", "title": "An artwork", "aliases": [], "publication_status": "unverified"}]
        self.data["compositions"] = [{"id": "composition-001", "artwork_id": "work-001"}]
        self.data["editions"] = [{"id": "edition-001", "composition_id": "composition-001"}]

    def test_valid_distinct_identities_and_owner_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "frames.py").touch()
            self.assertEqual(implementation.validate(self.data, directory)["counts"]["artworks"], 1)

    def test_invalid_typed_reference_rejected(self):
        for kind, field, bad in (("modules", "capability_ids", ["work-001"]), ("compositions", "artwork_id", "composition-001"), ("editions", "composition_id", "work-001")):
            data = copy.deepcopy(self.data)
            data[kind][0][field] = bad
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                implementation.validate(data)

    def test_artwork_alias_cannot_name_software(self):
        self.data["artworks"][0]["aliases"] = ["frame-compositor"]
        with self.assertRaisesRegex(ValueError, "artwork"):
            implementation.validate(self.data)

    def test_missing_module_and_escape_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Unresolved"):
                implementation.validate(self.data, directory)
        self.data["modules"][0]["path"] = "../another-owner/source.py"
        with self.assertRaisesRegex(ValueError, "escapes"):
            implementation.validate(self.data)

    def test_duplicate_identity_and_unverified_publication_rejected(self):
        self.data["capabilities"] *= 2
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            implementation.validate(self.data)
        self.data["capabilities"].pop()
        del self.data["artworks"][0]["publication_status"]
        with self.assertRaisesRegex(ValueError, "publication_status"):
            implementation.validate(self.data)


if __name__ == "__main__":
    unittest.main()
