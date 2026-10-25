#!/usr/bin/env python3
"""Render and validate the ACE catalog; create non-destructive local views."""

import argparse
import hashlib
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


BOUNDARIES = {
    "backwards-up-hill": "Source binding missing; related footage referenced by time-moment-brief; independent source custody preservation required.",
    "cycles": "Verified Page image inventory; no public implementation repository resolved; preserve source collection.",
    "danse": "Canonical source in private repository with deterministic performance engine; archived public continuation distinct; verify engine test suite and maintain custody.",
    "etc": "Artwork record preserved; historical etceter4 site association unresolved; maintain separate identity.",
    "god-here": "Active implementation in audiovisual-media-postproduction-system; local preservation git repository retained separately.",
    "hole-loop": "Active implementation in timed-text-navigation-loop; compose timed text encounter with browser score.",
    "mavsoleum-a": "Active implementation in generative-multimedia-spatial-environment; historical website composition.",
    "noonlight": "Source-led artwork record; unversioned media custody required; implementation location unresolved.",
    "nrcsvs": "Research archive and chat vault (reflect-recur); local unversioned preservation; no public implementation repository.",
    "nvde": "Source-led artwork record; unversioned media custody required; implementation location unresolved.",
    "ogod": "Active implementation in generative-multimedia-spatial-environment; preserve shared source owner.",
    "passing-thru": "Source-led artwork record; unversioned media custody required; implementation location unresolved.",
    "simvltanea": "Active implementation in independent-loop-compositor; retain Python layout, editions, and loop composition.",
    "time-moment-brief": "Authoritative shared-engine and multicamera playback repository; restricted implementation; independent custody required.",
    "wrvng-v": "Source-led artwork record; unversioned media custody required; implementation location unresolved.",
}

REQUIRED_BASELINE_PRS = {
    "audiovisual-composition-system": (15, 16, 17, 18),
    "audiovisual-media-postproduction-system": (118, 119, 120),
    "simvltanea": (34, 35, 36),
    "time-moment-brief": (18, 19, 20),
    "timed-text-navigation-loop": (65, 66, 67, 68),
    "generative-multimedia-spatial-environment": (183, 184, 185),
    "the-thing-without-a-name-screendance": (72, 73, 74, 75),
}

EXPECTED_ACTIVE_REPOS = tuple(REQUIRED_BASELINE_PRS.keys())

EXPECTED_SOURCE_LED_WORKS = (
    "backwards-up-hill",
    "cycles",
    "etc",
    "noonlight",
    "nrcsvs",
    "nvde",
    "passing-thru",
    "wrvng-v",
)


def verify_native_admission_status(manifest_data=None):
    """Verify operator-authorized native admission override and Wave 1-3 merged baseline."""
    if manifest_data is None:
        continuation_path = REPOSITORY / "manifests" / "project-continuation.json"
        if not continuation_path.is_file():
            return {
                "status": "FAIL",
                "admission_status": "missing",
                "external_broker_waived": False,
                "policy_priority_override": False,
                "baseline_repositories_verified": 0,
                "baseline_prs_verified": 0,
                "errors": [f"Missing continuation manifest: {continuation_path}"],
            }
        manifest_data = json.loads(continuation_path.read_text(encoding="utf-8"))
    elif isinstance(manifest_data, (str, Path)):
        p = Path(manifest_data)
        if not p.is_file():
            return {
                "status": "FAIL",
                "admission_status": "missing",
                "external_broker_waived": False,
                "policy_priority_override": False,
                "baseline_repositories_verified": 0,
                "baseline_prs_verified": 0,
                "errors": [f"Missing continuation manifest: {p}"],
            }
        manifest_data = json.loads(p.read_text(encoding="utf-8"))

    errors = []
    admission = manifest_data.get("native_admission", {})
    adm_status = admission.get("admission_status")
    broker_waived = bool(admission.get("external_broker_waived", False))
    priority_override = bool(admission.get("policy_priority_override", False))

    if adm_status != "admitted_operator_override":
        errors.append(f"Invalid admission_status: expected 'admitted_operator_override', got '{adm_status}'")
    if not broker_waived:
        errors.append("external_broker_waived must be true")
    if not priority_override:
        errors.append("policy_priority_override must be true")

    baseline = manifest_data.get("merged_trunk_baseline", {})
    verified_repos = {}
    total_prs = 0
    for repo_name, expected_prs in REQUIRED_BASELINE_PRS.items():
        repo_data = baseline.get(repo_name)
        if not repo_data:
            errors.append(f"Missing merged baseline record for repository: {repo_name}")
            continue
        merged_prs = tuple(repo_data.get("merged_prs", ()))
        if merged_prs != expected_prs:
            errors.append(
                f"Merged PR mismatch for {repo_name}: expected {list(expected_prs)}, got {list(merged_prs)}"
            )
        else:
            verified_repos[repo_name] = {
                "full_name": repo_data.get("full_name"),
                "merged_prs": list(merged_prs),
                "baseline_status": repo_data.get("baseline_status"),
            }
            total_prs += len(merged_prs)

    is_valid = len(errors) == 0
    return {
        "status": "PASS" if is_valid else "FAIL",
        "admission_status": adm_status,
        "external_broker_waived": broker_waived,
        "policy_priority_override": priority_override,
        "baseline_repositories_verified": len(verified_repos),
        "baseline_prs_verified": total_prs,
        "details": {
            "admission": admission,
            "repositories": verified_repos,
        },
        "errors": errors,
    }


def audit_estate_wave_progression(manifest_data=None, source_led_data=None):
    """Audit full estate cross-wave progression across 8 source-led works and 7 active repositories.

    Guarantees 15/15 complete estate coverage without omissions.
    """
    errors = []

    # 1. Resolve manifest_data (project-continuation.json)
    if manifest_data is None:
        p = REPOSITORY / "manifests" / "project-continuation.json"
        if not p.is_file():
            errors.append(f"Missing continuation manifest: {p}")
            manifest_data = {}
        else:
            manifest_data = json.loads(p.read_text(encoding="utf-8"))
    elif isinstance(manifest_data, (str, Path)):
        p = Path(manifest_data)
        if not p.is_file():
            errors.append(f"Missing continuation manifest: {p}")
            manifest_data = {}
        else:
            manifest_data = json.loads(p.read_text(encoding="utf-8"))

    # 2. Resolve source_led_data (source-led-continuation-records.json)
    if source_led_data is None:
        p = REPOSITORY / "manifests" / "source-led-continuation-records.json"
        if not p.is_file():
            errors.append(f"Missing source-led records manifest: {p}")
            source_led_data = {}
        else:
            source_led_data = json.loads(p.read_text(encoding="utf-8"))
    elif isinstance(source_led_data, (str, Path)):
        p = Path(source_led_data)
        if not p.is_file():
            errors.append(f"Missing source-led records manifest: {p}")
            source_led_data = {}
        else:
            source_led_data = json.loads(p.read_text(encoding="utf-8"))

    # 3. Check active repositories
    baseline = manifest_data.get("merged_trunk_baseline", {})
    wave_progressions = {}
    found_active = []
    for repo_name in EXPECTED_ACTIVE_REPOS:
        repo_info = baseline.get(repo_name)
        if not repo_info:
            errors.append(f"Missing active repository from merged trunk baseline: {repo_name}")
        else:
            found_active.append(repo_name)
            wave_progressions[repo_name] = {
                "type": "active_repository",
                "full_name": repo_info.get("full_name"),
                "merged_prs": repo_info.get("merged_prs", []),
                "baseline_status": repo_info.get("baseline_status", "merged"),
            }

    # 4. Check source-led works
    works = source_led_data.get("works", {})
    found_source_led = []
    for work_name in EXPECTED_SOURCE_LED_WORKS:
        work_info = works.get(work_name)
        if not work_info:
            errors.append(f"Missing source-led work from continuation records: {work_name}")
        else:
            found_source_led.append(work_name)
            wave_progressions[work_name] = {
                "type": "source_led_work",
                "stable_project_id": work_info.get("stable_project_id"),
                "work_type": work_info.get("work_type"),
                "binding_status": work_info.get("binding_status", "unbound"),
            }

    total_projects = len(found_active) + len(found_source_led)
    coverage_complete = (len(errors) == 0) and (total_projects == 15) and (len(found_active) == 7) and (len(found_source_led) == 8)

    return {
        "status": "PASS" if coverage_complete else "FAIL",
        "total_projects": total_projects,
        "source_led_count": len(found_source_led),
        "active_repo_count": len(found_active),
        "wave_progressions": wave_progressions,
        "coverage_complete": coverage_complete,
        "errors": errors,
    }


def generate_estate_completion_seal(manifest_data=None, source_led_data=None) -> dict:
    """Generate a canonical SHA-256 digested estate completion seal across all 15 projects."""
    audit = audit_estate_wave_progression(manifest_data=manifest_data, source_led_data=source_led_data)
    ready = bool(audit.get("coverage_complete", False) and len(audit.get("errors", [])) == 0)

    seal = {
        "schema": "ace.estate_completion_seal.v1",
        "ready": ready,
        "total_projects": audit.get("total_projects", 0),
        "active_repos": audit.get("active_repo_count", 0),
        "source_led_works": audit.get("source_led_count", 0),
        "wave_progressions": audit.get("wave_progressions", {}),
        "errors": audit.get("errors", []),
    }

    payload_to_hash = {k: v for k, v in seal.items() if k not in ("seal_digest", "digest")}
    canonical_bytes = json.dumps(payload_to_hash, sort_keys=True).encode("utf-8")
    seal_digest = hashlib.sha256(canonical_bytes).hexdigest()

    seal["seal_digest"] = seal_digest
    seal["digest"] = seal_digest
    return seal


def rendered_files(manifest):
    """Generate only the conservative public projection; local bindings stay ignored."""
    catalog = public_catalog(manifest)
    files = {}
    repos = {repo["key"]: repo for repo in catalog["repositories"]}
    registry = catalog["identity_registry"]
    entities = {item["id"]: item for group, items in registry.items()
                if isinstance(items, list) for item in items}
    manifest_by_slug = {p["slug"]: p for p in manifest["projects"]}
    rows = []
    for project in catalog["projects"]:
        slug = project["slug"]
        orig_project = manifest_by_slug.get(slug, project)
        source_state = orig_project.get("source_state", project.get("source_state", "metadata-only"))
        identity = project.get("identity_ref") or orig_project.get("identity_ref")
        if identity:
            ref_display = f"`{identity['type']}:{identity['id']}`"
        else:
            ref_display = "none (unresolved)"
        boundary = BOUNDARIES.get(slug, "Public continuation boundary defined by owning repository or custody plan.")
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
                f"- Source state: `{source_state}`\n"
                f"- Identity / reference: {ref_display}\n"
                f"- Public implementation: {'; '.join(links) or 'not disclosed or not resolved'}\n"
                f"- Start Here / Continuation: {boundary}\n")
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
                    f"{project['profile']} | `{source_state}` | {ref_display} | "
                    f"{'; '.join(links) or 'not disclosed or unresolved'} | {boundary} |")
    files["docs/project-catalog.md"] = (
        "# ACE project catalog\n\nGenerated public projection of 15 stable project records. "
        "Artistic titles and legacy project aliases identify works and membership records. "
        "Private source relationships, Page links and workstation bindings are excluded. "
        "Unverified publication status does not assert release acceptance.\n\n"
        "## Start Here / Continuation Summary\n\n"
        "- **Source-led works (T12)**: `backwards-up-hill`, `cycles`, `noonlight`, `nrcsvs`, `nvde`, `passing-thru`, and `wrvng-v` "
        "represent source-media-led artworks and research vaults. Where local bindings are missing or page-record-only, custody preservation "
        "and independent asset tracking govern continuation rather than code implementation.\n"
        "- **Public implementations**: `god-here` (audiovisual-media-postproduction-system), `hole-loop` (timed-text-navigation-loop), "
        "`mavsoleum-a` and `ogod` (generative-multimedia-spatial-environment), and `simvltanea` (independent-loop-compositor) possess active public implementation repositories.\n"
        "- **Restricted implementations**: `danse` (deterministic-performance-engine) and `time-moment-brief` (synchronized-generation-playback) "
        "remain in private repositories with independent custody and verification gates.\n"
        "- **Native admission & merged trunk baseline**: Operator-authorized native admission override (`admitted_operator_override`, external broker waived, policy priority override). "
        "Wave 1–2 trunk baseline merged across all 6 implementation repositories (`audiovisual-composition-system` PRs #15/#16, `audiovisual-media-postproduction-system` PR #118, "
        "`simvltanea` PR #34, `time-moment-brief` PR #18, `timed-text-navigation-loop` PR #65, `generative-multimedia-spatial-environment` PR #183, `the-thing-without-a-name-screendance` PR #72).\n\n"
        "| Work or project | Stable project ID | Record profile | Source state | Identity / reference | Public implementation | Start Here / Continuation |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(rows) + "\n")
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
    parser.add_argument("command", choices=("render", "check", "plan", "apply", "status", "audit-progression", "seal"))
    parser.add_argument("--catalog-only", action="store_true", help="CI: allow absent ignored workstation sources")
    args = parser.parse_args()
    if args.catalog_only and args.command != "check":
        parser.error("--catalog-only is only valid with check")
    manifest = load_manifest()
    if args.command == "status":
        print(json.dumps(source_status(manifest), indent=2))
        return
    if args.command == "audit-progression":
        result = audit_estate_wave_progression()
        print(json.dumps(result, indent=2))
        if result["status"] != "PASS":
            sys.exit(1)
        return
    if args.command == "seal":
        result = generate_estate_completion_seal()
        print(json.dumps(result, indent=2))
        if not result["ready"]:
            sys.exit(1)
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
