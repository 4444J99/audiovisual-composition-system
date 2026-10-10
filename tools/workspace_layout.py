#!/usr/bin/env python3
"""Render and validate the ACE catalog; create non-destructive local views."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile


REPOSITORY = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def safe_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value:
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
    if manifest["schema_version"] != "1.0.0":
        raise ValueError("Unsupported manifest contract")
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
    return files


def planned_links(manifest, workspace):
    links = []
    for group in ("projects", "repositories", "components", "archives"):
        links.append((workspace / group, REPOSITORY / group))
    links.append((workspace / "audiovisual-composition-system.code-workspace",
                  REPOSITORY / "audiovisual-composition-system.code-workspace"))
    links.append((workspace.parent / manifest["legacy_workspace_alias"], workspace))
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
    for link, target in links:
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("render", "check", "plan", "apply"))
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    manifest = load_manifest()
    files = rendered_files(manifest)
    if args.command == "render":
        # Preflight every destination before any write.
        paths = {relative: render_path(relative) for relative in files}
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
        path = REPOSITORY / relative
        if not path.is_file() or path.read_text() != content:
            raise ValueError(f"Stale generated view: {relative}; run render")
    if args.command in ("apply", "plan") and not args.workspace:
        raise ValueError("Explicit --workspace is required")
    count = 0
    if args.workspace:
        workspace = args.workspace.resolve()
        if REPOSITORY.parent != workspace or REPOSITORY.name != "system":
            raise ValueError("Coordination checkout must be WORKSPACE/system")
        links = planned_links(manifest, workspace)
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
