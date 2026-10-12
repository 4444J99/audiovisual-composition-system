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


REPOSITORY = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def safe_path(value):
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
    if manifest["schema_version"] != "2.0.0" or manifest.get("layout") != "workspace-root":
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
    return manifest


def rendered_files(manifest):
    files = {}
    rows = []
    repos = {repo["key"]: repo for repo in manifest["repositories"]}
    for project in manifest["projects"]:
        slug = project["slug"]
        source_links = []
        for key in project["repository_keys"]:
            repo = repos[key]
            url = "https://github.com/" + repo["full_name"]
            if project["repository_subpath"]:
                url += "/tree/main/" + project["repository_subpath"]
            source_links.append(f"[{repo['full_name']}]({url})")
        local = [f"[{name}](local/{name})" for name in project["local_bindings"]]
        files[f"projects/{slug}/README.md"] = (
            f"# {project['title']}\n\n"
            "Generated from `workspace-manifest.json`; update that record and rerender.\n\n"
            f"{project['decision']}\n\n"
            f"- Stable source identity: `{project['id']}`\n"
            f"- Canonical project slug: `{slug}`\n"
            f"- Profile: `{project['profile']}`\n"
            f"- Observed source state: `{project['source_state']}`\n"
            f"- Aliases: {', '.join(project['aliases']) or 'none recorded'}\n"
            f"- [Project Page]({project['page_url']})\n"
            f"- [Original ChatGPT project](https://chatgpt.com/g/{project['id']}/project)\n"
            f"- Implementation: {'; '.join(source_links) or 'not resolved in the bounded inventory'}\n"
            f"- Local navigation: {', '.join(local) or 'no local binding; use the source Page'}\n\n"
            "Local links are generated, ignored navigation only. The linked source retains "
            "its Git history, handling restrictions and authoritative metadata.\n"
        )
        rows.append(f"| [{slug}](../projects/{slug}/README.md) | {project['profile']} | "
                    f"{'; '.join(source_links) or 'Page record'} | "
                    f"{', '.join(project['local_bindings'].values()) or 'unresolved locally'} |")
    files["docs/project-catalog.md"] = (
        "# ACE project catalog\n\n"
        "Generated from the solution manifest. The source directory's 16 rows represent "
        "15 distinct project IDs; its repeated god-here row is one record. "
        "An unresolved local binding is not evidence that no source exists elsewhere.\n\n"
        "| Project | Profile | Implementation owner | Current local source |\n"
        "| --- | --- | --- | --- |\n" + "\n".join(rows) + "\n"
    )
    for group, keyfield in (("repositories", "key"), ("components", "slug"), ("archives", "slug")):
        for item in manifest[group]:
            name = item[keyfield]
            body = f"# {name}\n\nGenerated from the solution manifest.\n\n{item['role']}\n\n"
            if item.get("full_name"):
                body += f"[Repository](https://github.com/{item['full_name']}) · GitHub ID `{item['github_id']}`\n\n"
            if item.get("version_control"):
                body += f"Version control: `{item['version_control']}`.\n\n"
            body += ("[Existing local source](local/source).\n" if item.get("local_path")
                     else "Remote source is referenced; no duplicate checkout was created.\n")
            if item.get("authority_state"):
                body += "\n" + item["authority_state"] + ".\n"
            files[f"{group}/{name}/README.md"] = body
    folders = [{"name": "Workspace", "path": "."}]
    folders += [{"name": group.title(), "path": group}
                for group in ("projects", "repositories", "components", "archives")]
    files["audiovisual-composition-system.code-workspace"] = json.dumps({
        "folders": folders,
        "settings": {"search.followSymlinks": False, "files.watcherExclude": {
            "**/local/**": True}, "git.autoRepositoryDetection": "openEditors"}
    }, indent=2) + "\n"
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
                links.append((REPOSITORY / group / item[keyfield] / "local/source",
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
        result = subprocess.run(["git", "-C", str(REPOSITORY), "check-ignore", "--no-index", "--quiet", "--", value], capture_output=True)
        if result.returncode != 0:
            raise ValueError(f"Source is not ignored: {value}")
    for link, _ in planned_links(manifest):
        if link.is_relative_to(REPOSITORY):
            relative = link.relative_to(REPOSITORY).as_posix()
            result = subprocess.run(["git", "-C", str(REPOSITORY), "check-ignore",
                                     "--no-index", "--quiet", "--", relative], capture_output=True)
            if result.returncode != 0:
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
