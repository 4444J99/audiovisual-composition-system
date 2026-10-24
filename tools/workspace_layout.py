#!/usr/bin/env python3
"""Render and validate the ACE catalog; create non-destructive local views."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

# Also support importlib-based safety tests loading this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from identity_contract import public_catalog, validate_manifest


REPOSITORY = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def safe_path(value):
    # A control character (LF/CR above all) would split one manifest value into
    # several generated .gitignore directives, so reject it before building a path.
    if CONTROL.search(value):
        raise ValueError(f"Nonportable workspace binding: {value!r}")
    path = PurePosixPath(value)
    if not value or str(path) == "." or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError(f"Nonportable workspace binding: {value!r}")
    return path


def load_manifest():
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    manifest = json.loads((REPOSITORY / "workspace-manifest.json").read_text(),
                          object_pairs_hook=unique_pairs)
    if manifest["schema_version"] != "2.1.0" or manifest.get("layout") != "workspace-root":
        raise ValueError("Unsupported manifest contract")
    for entry in manifest["root_entries"] + manifest["preserved_root_files"]:
        if len(safe_path(entry).parts) != 1:
            raise ValueError(f"Root entry must be top-level: {entry}")
    projects = manifest["projects"]
    if not SLUG.fullmatch(manifest["legacy_workspace_alias"]):
        raise ValueError("Invalid legacy workspace alias")
    source = json.loads((REPOSITORY / str(safe_path(manifest["membership_source"]))).read_text(),
                        object_pairs_hook=unique_pairs)
    if source["distinct_count"] != len(projects):
        raise ValueError("Project count differs from observed source membership")
    observed = {(p["id"], p["slug"], p["page_id"]) for p in source["projects"]}
    declared = {(p["id"], p["slug"], p["page_id"]) for p in projects}
    if observed != declared:
        raise ValueError("Project membership differs from observed source identities")
    for field in ("id", "slug", "page_id"):
        values = [project[field].casefold() for project in projects]
        if len(set(values)) != len(values):
            raise ValueError(f"Duplicate project {field}")
    keys = [repo["key"] for repo in manifest["repositories"]]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate repository key")
    if any(not SLUG.fullmatch(key) for key in keys):
        raise ValueError("Invalid repository directory key")
    labels = {}
    for project in projects:
        for label in [project["slug"], *project["aliases"]]:
            normalized = label.casefold()
            if normalized in labels and labels[normalized] != project["id"]:
                raise ValueError(f"Ambiguous project alias: {label}")
            labels[normalized] = project["id"]
    for group in (projects, manifest["components"], manifest["archives"]):
        slugs = [item["slug"] for item in group]
        if len(slugs) != len(set(slugs)):
            raise ValueError("Duplicate directory slug")
        for slug in slugs:
            if not SLUG.fullmatch(slug) or len(slug) > 100:
                raise ValueError(f"Invalid directory slug: {slug}")
    for project in projects:
        if any(key not in keys for key in project["repository_keys"]):
            raise ValueError(f"Unresolved repository for {project['slug']}")
        for name, target in project["local_bindings"].items():
            if not SLUG.fullmatch(name):
                raise ValueError(f"Invalid binding name: {name}")
            safe_path(target)
    for group in (manifest["repositories"], manifest["components"], manifest["archives"]):
        for item in group:
            if item.get("version_control", "unversioned") not in ("git", "unversioned"):
                raise ValueError("Invalid source version_control")
            if item.get("local_path"):
                safe_path(item["local_path"])
    validate_manifest(manifest)
    return manifest


def rendered_files(manifest):
    """Generate only the conservative public projection; local bindings stay ignored."""
    catalog = public_catalog(manifest)
    files = {}
    repos = {repo["key"]: repo for repo in catalog["repositories"]}
    registry = catalog["identity_registry"]
    entities = {item["id"]: item for group, items in registry.items()
                if isinstance(items, list) for item in items}
    rows = []
    for project in catalog["projects"]:
        slug = project["slug"]
        identity = project.get("identity_ref")
        canonical = f"artworks/{identity['id']}" if identity and identity["type"] == "artwork" else f"projects/{slug}"
        links = []
        for key in project["repository_keys"]:
            repo = repos[key]
            url = "https://github.com/" + repo["full_name"]
            links.append(f"[{repo.get('directory_slug', key)}]({url})")
        body = (f"# {project['title']}\n\n"
                "Generated from the public identity catalog.\n\n"
                f"- Stable project ID: `{project['id']}`\n"
                f"- Legacy project alias: `{slug}`\n"
                f"- Record profile: `{project['profile']}`\n"
                f"- Public implementation: {'; '.join(links) or 'not disclosed or not resolved'}\n")
        if identity and identity["type"] == "artwork":
            body += (f"- Artwork ID: `{identity['id']}`\n"
                     f"- Publication status: `{entities[identity['id']]['publication_status']}`\n\n"
                     "Artistic titles identify works. Reusable software uses its own functional identity.\n")
            files[f"{canonical}/README.md"] = body
            files[f"projects/{slug}/README.md"] = (
                f"# {project['title']}\n\nLegacy project navigation, retained for compatibility.\n\n"
                f"[Canonical artwork record](../../{canonical}/README.md) · "
                f"Stable project ID `{project['id']}`.\n\n"
                "This alias is not a software module or a source-media identifier.\n")
        else:
            files[f"projects/{slug}/README.md"] = body + "\nThis membership record is not asserted to be an artwork.\n"
        rows.append(f"| [{project['title']}](../{canonical}/README.md) | `{project['id']}` | "
                    f"{project['profile']} | {'; '.join(links) or 'not disclosed or unresolved'} |")
    files["docs/project-catalog.md"] = (
        "# ACE project catalog\n\nGenerated public projection of 15 stable project records. "
        "Artistic titles and legacy project aliases identify works and membership records. "
        "Private source relationships, Page links and workstation bindings are excluded. "
        "Unverified publication status does not assert release acceptance.\n\n"
        "| Work or project | Stable project ID | Record profile | Public implementation |\n"
        "| --- | --- | --- | --- |\n" + "\n".join(rows) + "\n")
    for group, keyfield in (("repositories", "key"), ("components", "slug"), ("archives", "slug")):
        for item in catalog[group]:
            legacy = item[keyfield]
            canonical = item.get("directory_slug", legacy)
            body = f"# {canonical}\n\nGenerated public navigation.\n\n{item['role']}\n\n"
            if item.get("full_name"):
                body += f"[Repository](https://github.com/{item['full_name']}) · Stable GitHub ID `{item['github_id']}`.\n\n"
            if item.get("software_ref"):
                body += f"Software identity: `{item['software_ref']['id']}`.\n\n"
            body += "Original source placement, interfaces and independent histories are retained.\n"
            files[f"{group}/{canonical}/README.md"] = body
            if canonical != legacy:
                files[f"{group}/{legacy}/README.md"] = (
                    f"# Compatibility navigation\n\n"
                    f"[Canonical functional record](../{canonical}/README.md).\n\n"
                    f"Legacy key `{legacy}` is retained for existing consumers. "
                    "No source media or repository history moved.\n")
    software_rows = []
    for software in registry["software_systems"]:
        software_rows.append(f"| `{software['id']}` | {software['responsibility']} |")
    module_rows = []
    for module in registry["modules"]:
        capabilities = ", ".join(f"`{ref['id']}`" for ref in module["capability_refs"])
        module_rows.append(f"| `{module['software_ref']['id']}` | `{module['native_id']}` | "
                           f"`{module['path']}` | {capabilities} | "
                           f"{module.get('reuse_status', 'interfaces-preserved')} |")
    files["docs/software-catalog.md"] = (
        "# ACE software and capability catalog\n\nGenerated from public identity records. "
        "Implementation paths and interfaces remain owned by their repositories. Migration "
        "contracts are review-pending until their implementation branches are merged; "
        "this catalog does not assert deployment or media acceptance. Private implementation "
        "details remain in their private owners.\n\n"
        "| Software system | Processing responsibility |\n| --- | --- |\n" +
        "\n".join(software_rows) + "\n\n"
        "| Software owner | Module | Existing or compatibility path | Capabilities | Reuse status |\n"
        "| --- | --- | --- | --- | --- |\n" + "\n".join(module_rows) + "\n")
    files["docs/public-catalog.json"] = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    folders = [{"name": "Workspace", "path": "."}]
    folders += [{"name": group.title(), "path": group}
                for group in ("artworks", "projects", "repositories", "components", "archives")]
    files["audiovisual-composition-system.code-workspace"] = json.dumps({
        "folders": folders,
        "settings": {"search.followSymlinks": False, "files.watcherExclude": {
            "**/local/**": True}, "git.autoRepositoryDetection": "openEditors"}
    }, indent=2) + "\n"
    # Existing ignore rules preserve custody of already-declared workstation
    # sources. They are not part of the portable public JSON/catalog projection.
    files[".gitignore"] = rendered_ignore(manifest)
    return files


def planned_links(manifest):
    workspace = REPOSITORY
    links = [(workspace.parent / manifest["legacy_workspace_alias"], workspace)]
    for project in manifest["projects"]:
        for name, target in project["local_bindings"].items():
            links.append((REPOSITORY / "projects" / project["slug"] / "local" / name,
                          workspace / str(safe_path(target))))
    for group, keyfield in (("repositories", "key"), ("components", "slug"), ("archives", "slug")):
        for item in manifest[group]:
            if item.get("local_path"):
                names = {item[keyfield], item.get("directory_slug", item[keyfield])}
                for name in sorted(names):
                    links.append((REPOSITORY / group / name / "local/source",
                                  workspace / str(safe_path(item["local_path"]))))
    return links


def inspect_links(links, require_existing):
    missing = []
    root = REPOSITORY.resolve()
    for link, target in links:
        legacy = link.parent == root.parent and target == root
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"Source escapes workspace root: {target}")
        if not legacy and not link.absolute().is_relative_to(root):
            raise ValueError(f"Link escapes workspace root: {link}")
        if not target.exists():
            raise ValueError(f"Missing bound source: {target}")
        if os.path.lexists(link):
            if not link.is_symlink() or link.resolve() != target.resolve():
                raise ValueError(f"Refusing occupied or mismatched destination: {link}")
        else:
            missing.append((link, target))
        # Never create a path through an existing symlinked parent.
        parent = link.parent
        while parent != parent.parent and parent != REPOSITORY and parent != target.parent:
            if parent.is_symlink():
                raise ValueError(f"Refusing symlinked destination parent: {parent}")
            parent = parent.parent
    if require_existing and missing:
        raise ValueError(f"Missing {len(missing)} local navigation links; run apply")
    return missing


def render_path(relative):
    path = REPOSITORY / str(safe_path(relative))
    if not path.resolve().is_relative_to(REPOSITORY):
        raise ValueError(f"Render path escapes repository: {relative}")
    for candidate in [path, *path.parents]:
        if candidate == REPOSITORY:
            break
        if candidate.is_symlink():
            raise ValueError(f"Refusing symlinked render path: {candidate}")
    return path


def source_paths(manifest):
    paths = set(manifest["preserved_root_files"])
    for project in manifest["projects"]:
        paths.update(project["local_bindings"].values())
    for group in ("repositories", "components", "archives"):
        paths.update(item["local_path"] for item in manifest[group] if item.get("local_path"))
    for value in paths:
        if len(safe_path(value).parts) != 1:
            raise ValueError(f"Source must be top-level: {value}")
    if paths.intersection(manifest["root_entries"]):
        raise ValueError("Source overlaps authored or generated root entry")
    return sorted(paths)


def rendered_ignore(manifest):
    path = render_path(".gitignore")
    content = path.read_text() if path.exists() else ""
    begin, end = "# BEGIN generated sources", "# END generated sources"
    if begin in content or end in content:
        if content.count(begin) != 1 or content.count(end) != 1:
            raise ValueError("Malformed generated sources block")
        before, rest = content.split(begin)
        _, after = rest.split(end)
        if after.strip():
            raise ValueError("Generated sources block must be last")
        content = before
    # Literal, anchored Git patterns (including spaces in original archive names).
    patterns = []
    for value in source_paths(manifest):
        escaped = re.sub(r"([\\*?\[\]#! ])", r"\\\1", value)
        patterns.append("/" + escaped)
    return content.rstrip() + "\n\n" + begin + "\n" + "\n".join(patterns) + "\n" + end + "\n"


def git_output(source, *args):
    result = subprocess.run(["git", "--no-optional-locks", "-C", str(source), *args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"Git failed: {args}")
    return result.stdout.strip()


def source_status(manifest):
    records = []
    for value in source_paths(manifest):
        source = REPOSITORY / value
        if not source.resolve().is_relative_to(REPOSITORY):
            raise ValueError(f"Source escapes workspace root: {value}")
        record = {"source": value}
        if not source.exists():
            record["state"] = "missing"
        elif not (source / ".git").exists():
            record["state"] = "unversioned"
        else:
            record.update(state="git", branch=git_output(source, "branch", "--show-current") or "DETACHED",
                          head=git_output(source, "rev-parse", "HEAD"),
                          uncommitted_files=len(git_output(source, "status", "--porcelain=v1", "--untracked-files=all").splitlines()),
                          worktrees=git_output(source, "worktree", "list", "--porcelain").count("worktree "))
            upstream = subprocess.run(["git", "--no-optional-locks", "-C", str(source), "rev-parse", "--verify", "@{upstream}"], capture_output=True)
            record.update(ahead=None, behind=None)
            if upstream.returncode == 0:
                ahead, behind = git_output(source, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
                record.update(ahead=int(ahead), behind=int(behind))
        records.append(record)
    return records


def repository_ignored(relative):
    result = subprocess.run(["git", "-C", str(REPOSITORY), "check-ignore",
                             "--no-index", "--verbose", "-z", "--stdin"],
                            input=relative.encode() + b"\0", capture_output=True)
    fields = result.stdout.split(b"\0")
    return (result.returncode == 0 and len(fields) >= 4
            and fields[0] == b".gitignore" and not fields[2].startswith(b"!"))


def check_workspace(manifest, catalog_only=False):
    sources = source_paths(manifest)
    allowed = set(manifest["root_entries"]) | set(sources)
    unknown = sorted(p.name for p in REPOSITORY.iterdir() if p.name not in allowed)
    if unknown:
        raise ValueError(f"Undeclared root entries: {unknown}")
    for value in sources:
        source = REPOSITORY / value
        if not source.resolve().is_relative_to(REPOSITORY):
            raise ValueError(f"Source escapes workspace root: {value}")
        if not catalog_only and not source.exists():
            raise ValueError(f"Missing declared source: {value}")
        if not repository_ignored(value):
            raise ValueError(f"Source is not ignored: {value}")
    for link, _ in planned_links(manifest):
        if link.is_relative_to(REPOSITORY):
            relative = link.relative_to(REPOSITORY).as_posix()
            if not repository_ignored(relative):
                raise ValueError(f"Navigation link is not ignored: {relative}")
    git_sources = {item["local_path"] for group in ("repositories", "components", "archives")
                   for item in manifest[group] if item.get("local_path") and
                   (group == "repositories" or item.get("version_control") == "git")}
    for value in sorted(git_sources):
        path = REPOSITORY / value
        if (path.exists() or not catalog_only) and not (path / ".git").exists():
            raise ValueError(f"Repository source lacks .git: {path}")
        if path.exists():
            git_root = Path(git_output(path, "rev-parse", "--show-toplevel")).resolve()
            if git_root != path.resolve():
                raise ValueError(f"Repository source has wrong Git root: {path}")
            source_store = git_output(path, "rev-parse", "--path-format=absolute", "--git-common-dir")
            coordination_store = git_output(REPOSITORY, "rev-parse", "--path-format=absolute", "--git-common-dir")
            if Path(source_store).resolve() == Path(coordination_store).resolve():
                raise ValueError(f"Repository source shares coordination Git history: {path}")
    tracked = subprocess.check_output(["git", "-C", str(REPOSITORY), "ls-files", "-z"], text=True).split("\0")
    for value in filter(None, tracked):
        if PurePosixPath(value).parts[0] in sources:
            raise ValueError(f"Tracked source content: {value}")
        render_path(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("render", "check", "plan", "apply", "status"))
    parser.add_argument("--catalog-only", action="store_true", help="CI: allow absent ignored workstation sources")
    args = parser.parse_args()
    if args.catalog_only and args.command != "check":
        parser.error("--catalog-only is only valid with check")
    manifest = load_manifest()
    if args.command == "status":
        print(json.dumps(source_status(manifest), indent=2))
        return
    files = rendered_files(manifest)
    paths = {relative: render_path(relative) for relative in files}
    if args.command == "render":
        for relative, content in files.items():
            path = paths[relative]
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_text() != content:
                with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as temporary:
                    temporary.write(content)
                    temporary_path = Path(temporary.name)
                os.chmod(temporary_path, 0o644)
                temporary_path.replace(path)
        print(f"Rendered {len(files)} catalog files")
        return
    for relative, content in files.items():
        path = paths[relative]
        if not path.is_file() or path.read_text() != content:
            raise ValueError(f"Stale generated view: {relative}; run render")
    check_workspace(manifest, args.catalog_only)
    count = 0
    if not args.catalog_only:
        links = planned_links(manifest)
        missing = inspect_links(links, require_existing=args.command == "check")
        if args.command == "apply":
            for link, target in missing:
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(os.path.relpath(target, link.parent), target_is_directory=target.is_dir())
            inspect_links(links, require_existing=True)
            print(f"Created {len(missing)} links; existing source bytes untouched")
        elif args.command == "plan":
            for link, target in missing:
                print(f"LINK {link} -> {os.path.relpath(target, link.parent)}")
        count = len(links)
    print(f"PASS: {len(manifest['projects'])} unique projects, {len(manifest['repositories'])} "
          f"repository references, {len(files)} generated files, {count} local links")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
