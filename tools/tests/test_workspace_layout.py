"""Safety predicates for directory navigation and generated documents."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


MODULE = Path(__file__).resolve().parents[1] / "workspace_layout.py"
SPEC = importlib.util.spec_from_file_location("layout", MODULE)
layout = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(layout)


class LayoutSafety(unittest.TestCase):
    def test_path_escape_rejected(self):
        for value in ("../private", "/private", "x/../../secret", "x\\y", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                layout.safe_path(value)

    def test_regular_destination_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, destination = root / "source", root / "destination"
            source.mkdir()
            destination.write_text("preserve me")
            with self.assertRaises(ValueError):
                layout.inspect_links([(destination, source)], False)
            self.assertEqual(destination.read_text(), "preserve me")

    def test_wrong_alias_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, destination = root / "source", root / "destination"
            source.mkdir()
            destination.symlink_to("missing")
            with self.assertRaises(ValueError):
                layout.inspect_links([(destination, source)], False)
            self.assertEqual(destination.readlink(), Path("missing"))

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaises(ValueError):
                layout.inspect_links([(root / "destination", root / "missing")], False)
            self.assertFalse((root / "destination").exists())

    def test_correct_alias_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, destination = root / "source", root / "destination"
            source.mkdir()
            destination.symlink_to("source")
            self.assertEqual(layout.inspect_links([(destination, source)], True), [])

    def test_render_rejects_symlink_to_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "source.md").write_text("preserve original")
            (root / "README.md").symlink_to("source.md")
            with patch.object(layout, "REPOSITORY", root), self.assertRaises(ValueError):
                layout.render_path("README.md")
            self.assertEqual((root / "source.md").read_text(), "preserve original")

    def test_render_rejects_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "source").mkdir()
            (root / "docs").symlink_to("source")
            with patch.object(layout, "REPOSITORY", root), self.assertRaises(ValueError):
                layout.render_path("docs/new.md")

    def test_membership_matches_observed_identities(self):
        manifest = layout.load_manifest()
        self.assertEqual(len(manifest["projects"]), 15)
        self.assertEqual(len({p["id"] for p in manifest["projects"]}), 15)


if __name__ == "__main__":
    unittest.main()
