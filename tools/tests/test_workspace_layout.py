"""Safety predicates for directory navigation and generated documents."""

import importlib.util
from pathlib import Path, PurePosixPath
import tempfile
import subprocess
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

    def test_control_characters_rejected(self):
        for value in ("safe\n!/published-private", "safe\nREADME.md", "safe\n!published-private",
                      "safe\rextra", "safe\r\nextra", "safe\x00extra", "safe\x1fextra",
                      "safe\x7fextra", "safe\textra", "\n", "nested/safe\nextra"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                layout.safe_path(value)

    def test_valid_portable_bindings_still_accepted(self):
        for value in ("source", "Archive with spaces", "nested/source", "name-with.dots_and~marks"):
            with self.subTest(value=value):
                self.assertEqual(layout.safe_path(value), PurePosixPath(value))

    def test_ignore_block_cannot_gain_directives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.object(layout, "REPOSITORY", root):
                for value in ("safe\nREADME.md", "safe\n!published-private", "safe\rextra", "safe\r\nextra"):
                    manifest = {"root_entries": [], "preserved_root_files": [value],
                                "projects": [], "repositories": [], "components": [], "archives": []}
                    with self.subTest(value=value), self.assertRaises(ValueError):
                        layout.rendered_ignore(manifest)
                values = ["source", "Archive with spaces"]
                manifest = {"root_entries": [], "preserved_root_files": values,
                            "projects": [], "repositories": [], "components": [], "archives": []}
                block = layout.rendered_ignore(manifest).split("# BEGIN generated sources\n")[1]
                directives = block.split("# END generated sources")[0].splitlines()
                self.assertEqual(directives, ["/Archive\\ with\\ spaces", "/source"])

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
            with patch.object(layout, "REPOSITORY", root):
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

    def test_root_layout_links_and_legacy_alias(self):
        manifest = layout.load_manifest()
        self.assertEqual(manifest["layout"], "workspace-root")
        links = dict(layout.planned_links(manifest))
        self.assertEqual(links[layout.REPOSITORY / "projects/danse/local/checkout"],
                         layout.REPOSITORY / "the-thing-without-a-name")
        self.assertEqual(links[layout.REPOSITORY.parent / manifest["legacy_workspace_alias"]],
                         layout.REPOSITORY)
        self.assertNotIn(layout.REPOSITORY / "projects", links)

    def test_finder_metadata_does_not_hide_undeclared_root_entries(self):
        root_entries = layout.load_manifest()["root_entries"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".DS_Store\n")
            metadata = root / ".DS_Store"
            metadata.write_bytes(b"Finder metadata")
            manifest = {"root_entries": root_entries, "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace", "projects": [],
                        "repositories": [], "components": [], "archives": []}
            with patch.object(layout, "REPOSITORY", root):
                layout.check_workspace(manifest)
                self.assertEqual(metadata.read_bytes(), b"Finder metadata")
                (root / "unexpected").mkdir()
                with self.assertRaisesRegex(ValueError, "Undeclared.*unexpected"):
                    layout.check_workspace(manifest)

    def test_target_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory).resolve()
            (root / "source").symlink_to(Path(outside).resolve())
            with patch.object(layout, "REPOSITORY", root), self.assertRaisesRegex(ValueError, "escapes"):
                layout.inspect_links([(root / "local/source", root / "source")], False)

    def test_parent_symlink_rejected_before_apply(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "source").mkdir()
            (root / "local").symlink_to("source")
            with patch.object(layout, "REPOSITORY", root), self.assertRaisesRegex(ValueError, "parent"):
                layout.inspect_links([(root / "local/checkout", root / "source")], False)

    def test_workspace_checks_and_read_only_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            source = root / "source"
            subprocess.run(["git", "init", "-q", "-b", "main", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "--allow-empty", "-qm", "fixture"], check=True)
            (source / "dirty.txt").write_text("preserve me")
            (root / "Archive with spaces").mkdir()
            manifest = {"root_entries": [".git", ".gitignore"], "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace",
                        "projects": [], "repositories": [{"key": "source", "local_path": "source"}],
                        "components": [], "archives": [{"slug": "archive", "local_path": "Archive with spaces"}]}
            with patch.object(layout, "REPOSITORY", root):
                (root / ".gitignore").write_text("repositories/*/local/\narchives/*/local/\n")
                generated = layout.rendered_ignore(manifest)
                (root / ".gitignore").write_text(generated)
                self.assertEqual(layout.rendered_ignore(manifest), generated)
                layout.check_workspace(manifest)
                records = layout.source_status(manifest)
                record = next(r for r in records if r["source"] == "source")
                self.assertEqual(record["branch"], "main")
                self.assertEqual(record["uncommitted_files"], 1)
                self.assertEqual(record["worktrees"], 1)
                self.assertIsNone(record["ahead"])
                subprocess.run(["git", "-C", str(source), "branch", "upstream"], check=True)
                subprocess.run(["git", "-C", str(source), "branch", "--set-upstream-to=upstream"], check=True, capture_output=True)
                subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "--allow-empty", "-qm", "ahead"], check=True)
                record = next(r for r in layout.source_status(manifest) if r["source"] == "source")
                self.assertEqual((record["ahead"], record["behind"]), (1, 0))
                self.assertEqual((source / "dirty.txt").read_text(), "preserve me")
                (root / "unexpected").mkdir()
                with self.assertRaisesRegex(ValueError, "Undeclared"):
                    layout.check_workspace(manifest)
                (root / "unexpected").rmdir()
                (root / ".gitignore").write_text("")
                with self.assertRaisesRegex(ValueError, "not ignored"):
                    layout.check_workspace(manifest)
                (root / ".gitignore").write_text(generated)
                (root / "Archive with spaces").rmdir()
                with self.assertRaisesRegex(ValueError, "Missing declared source"):
                    layout.check_workspace(manifest)
                layout.check_workspace(manifest, catalog_only=True)
                self.assertEqual(layout.source_status(manifest)[0]["state"], "missing")

    def test_tracked_link_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "target").write_text("preserve")
            (root / "link").symlink_to("target")
            subprocess.run(["git", "-C", str(root), "add", "link"], check=True)
            manifest = {"root_entries": [".git", "target", "link"], "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace",
                        "projects": [], "repositories": [], "components": [], "archives": []}
            with patch.object(layout, "REPOSITORY", root), self.assertRaisesRegex(ValueError, "symlinked"):
                layout.check_workspace(manifest)

    def test_git_backed_archives_require_independent_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            archive = root / "archive"
            subprocess.run(["git", "init", "-q", str(archive)], check=True)
            manifest = {"root_entries": [".git", ".gitignore"], "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace", "projects": [],
                        "repositories": [], "components": [],
                        "archives": [{"slug": "archive", "local_path": "archive", "version_control": "git"}]}
            with patch.object(layout, "REPOSITORY", root):
                (root / ".gitignore").write_text("archives/*/local/\n")
                (root / ".gitignore").write_text(layout.rendered_ignore(manifest))
                for catalog_only in (False, True):
                    layout.check_workspace(manifest, catalog_only=catalog_only)
                (archive / ".git").rename(archive / "retained-git")
                for catalog_only in (False, True):
                    with self.subTest(catalog_only=catalog_only), self.assertRaisesRegex(ValueError, "lacks .git"):
                        layout.check_workspace(manifest, catalog_only=catalog_only)
                # A marker pointing to the containing coordination Git root is not independent history.
                (archive / ".git").write_text(f"gitdir: {root / '.git'}\n")
                with self.assertRaisesRegex(ValueError, "coordination Git history"):
                    layout.check_workspace(manifest)

    def test_navigation_ignores_checked_before_links_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            manifest = {"root_entries": [".git", ".gitignore"], "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace",
                        "projects": [{"slug": "example", "local_bindings": {"source": "source"}}],
                        "repositories": [{"key": "example", "local_path": "source"}],
                        "components": [{"slug": "example", "local_path": "source"}],
                        "archives": [{"slug": "example", "local_path": "source"}]}
            rules = [f"{group}/*/local/" for group in ("projects", "repositories", "components", "archives")]
            with patch.object(layout, "REPOSITORY", root):
                (root / ".gitignore").write_text("\n".join(rules) + "\n")
                generated = layout.rendered_ignore(manifest)
                (root / ".gitignore").write_text(generated)
                layout.check_workspace(manifest, catalog_only=True)
                for rule in rules:
                    for edited in (generated.replace(rule + "\n", ""),
                                   generated.replace("# BEGIN generated sources", "!" + rule + "\n# BEGIN generated sources")):
                        with self.subTest(rule=rule, edited=edited):
                            (root / ".gitignore").write_text(edited)
                            # Regeneration must not hide an unsafe hand-edited prefix.
                            (root / ".gitignore").write_text(layout.rendered_ignore(manifest))
                            with self.assertRaisesRegex(ValueError, "Navigation link is not ignored"):
                                layout.check_workspace(manifest, catalog_only=True)
                # Workstation-only exclusions must never substitute for clone-portable rules.
                for local in (False, True):
                    (root / ".gitignore").write_text(generated.replace(rules[0] + "\n", ""))
                    exclude = root / ".git" / ("info/exclude" if local else "global-exclude")
                    exclude.write_text(rules[0] + "\n")
                    if not local:
                        subprocess.run(["git", "-C", str(root), "config", "core.excludesFile", str(exclude)], check=True)
                    with self.assertRaisesRegex(ValueError, "Navigation link is not ignored"):
                        layout.check_workspace(manifest, catalog_only=True)

    def test_catalog_allows_missing_git_archive_but_strict_requires_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            manifest = {"root_entries": [".git", ".gitignore"], "preserved_root_files": [],
                        "legacy_workspace_alias": "legacy-workspace", "projects": [],
                        "repositories": [], "components": [],
                        "archives": [{"slug": "archive", "local_path": "archive", "version_control": "git"}]}
            with patch.object(layout, "REPOSITORY", root):
                (root / ".gitignore").write_text("archives/*/local/\n")
                (root / ".gitignore").write_text(layout.rendered_ignore(manifest))
                layout.check_workspace(manifest, catalog_only=True)
                with self.assertRaisesRegex(ValueError, "Missing declared source"):
                    layout.check_workspace(manifest)


if __name__ == "__main__":
    unittest.main()
