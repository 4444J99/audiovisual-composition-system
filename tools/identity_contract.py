#!/usr/bin/env python3
"""Typed ACE identity contract and conservative public catalog projection.

The authored manifest retains already-published legacy custody records. Their
sensitive subset is frozen; the public projection never exports those bindings.
Implementation contracts remain in the repositories that own their source.
"""

from copy import deepcopy
import hashlib
import json
from pathlib import PurePosixPath
import re

COLLECTIONS = {
    "software_systems": "software_system", "capabilities": "capability",
    "modules": "module", "source_media": "source_media",
    "compositions": "composition", "artworks": "artwork", "editions": "edition",
    "archives": "archive",
}
REF_TYPES = {
    "system_ref": "software_system", "software_ref": "software_system",
    "capability_refs": "capability", "artwork_ref": "artwork",
    "composition_ref": "composition", "source_media_refs": "source_media",
    "archive_ref": "archive",
}
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
COMMON_FIELDS = {"type", "id", "visibility"}
ENTITY_FIELDS = {
    "software_system": {"name", "responsibility", "repository_github_id", "implementation_contract", "integration_status"},
    "capability": {"native_id", "description"},
    "module": {"native_id", "software_ref", "path", "capability_refs", "interfaces", "reuse_status", "description", "compatibility_note"},
    "source_media": {"native_id", "label", "description", "content_digest", "provenance"},
    "composition": {"native_id", "software_ref", "artwork_ref", "path", "source_media_refs", "status", "description", "json_pointer"},
    "artwork": {"project_id", "title", "aliases", "publication_status"},
    "edition": {"native_id", "artwork_ref", "composition_ref", "version", "path", "json_pointer", "publication_status", "provenance"},
    "archive": {"legacy_slug", "description"},
}
PROVENANCE_FIELDS = {"repository_github_id", "record_path", "source_id", "original_name", "status"}
PRIVATE_SOFTWARE = {
    1408128309: ("synchronized-generation-playback", "Synchronized Generation Playback"),
    1320324017: ("deterministic-performance-engine", "Deterministic Performance Engine"),
}
# Captured from coordination main before migration 2.1.0. Changing this pin is a
# reviewed publication-contract migration, never part of rendering or discovery.
LEGACY_PRIVATE_SHA256 = "8b8d00ca7e0df9dcbdb006c146e49e4e75f304c81c8dd2cf2aa46161ff9bbf70"
LEGACY_PRIVATE_IDS = {1408128309, 1320324017}
REPOSITORY_ADDITIONS = {"directory_slug", "software_ref"}
PROJECT_ADDITIONS = {"identity_ref"}


def _required(record, *fields):
    for field in fields:
        if field not in record or record[field] in (None, ""):
            raise ValueError(f"Missing {field} in {record.get('id', record.get('key', 'record'))}")


def _portable_path(value):
    path = PurePosixPath(value)
    if not value or str(path) == "." or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError(f"Nonportable identity path: {value!r}")


def _ref(value, expected, records):
    if not isinstance(value, dict) or set(value) != {"type", "id"}:
        raise ValueError("A typed reference requires exactly type and id")
    if value["type"] != expected:
        raise ValueError(f"Wrong reference type: expected {expected}")
    if records.get(value["id"], {}).get("type") != expected:
        raise ValueError(f"Unresolved {expected} reference: {value['id']}")


def validate_registry(manifest):
    registry = manifest.get("identity_registry")
    if not isinstance(registry, dict) or registry.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported identity registry")
    if set(registry) != {"schema_version", *COLLECTIONS}:
        raise ValueError("Identity registry must declare all eight typed collections")
    records = {}
    for collection, kind in COLLECTIONS.items():
        if not isinstance(registry[collection], list):
            raise ValueError(f"Identity collection must be an array: {collection}")
        for record in registry[collection]:
            _required(record, "id", "type", "visibility")
            if record["type"] != kind:
                raise ValueError(f"Wrong entity type in {collection}")
            unknown = set(record) - COMMON_FIELDS - ENTITY_FIELDS[kind]
            if unknown:
                raise ValueError(f"Unknown {kind} fields: {sorted(unknown)}")
            structured = {"repository_github_id", "provenance", "aliases", "interfaces", *REF_TYPES}
            for key, value in record.items():
                if key not in structured and not isinstance(value, str):
                    raise ValueError(f"{kind}.{key} must be a string")
            for key in ("aliases", "interfaces"):
                if key in record and (not isinstance(record[key], list) or
                                      any(not isinstance(value, str) for value in record[key])):
                    raise ValueError(f"{kind}.{key} must be an array of strings")
            if "repository_github_id" in record and (type(record["repository_github_id"]) is not int or record["repository_github_id"] <= 0):
                raise ValueError("Repository identity must be a positive integer")
            if not ID.fullmatch(record["id"]):
                raise ValueError(f"Invalid identity: {record['id']}")
            if record["id"] in records:
                raise ValueError(f"Duplicate identity: {record['id']}")
            if record["visibility"] not in ("public", "restricted"):
                raise ValueError("Identity visibility must be explicit")
            records[record["id"]] = record
    repos = {r["github_id"]: r for r in manifest["repositories"]}
    if len(repos) != len(manifest["repositories"]):
        raise ValueError("Duplicate GitHub repository identity")
    project_ids = {p["id"] for p in manifest["projects"]}
    artwork_project_ids = set()
    for record in records.values():
        kind = record["type"]
        for key, value in record.items():
            if key.endswith(("_ref", "_refs")):
                if key not in REF_TYPES:
                    raise ValueError(f"Unknown typed relationship: {key}")
                if key.endswith("_refs"):
                    if not isinstance(value, list):
                        raise ValueError(f"Reference collection must be an array: {key}")
                    values = value
                else:
                    values = [value]
                for ref in values:
                    _ref(ref, REF_TYPES[key], records)
        if "path" in record:
            _portable_path(record["path"])
        if "implementation_contract" in record:
            _portable_path(record["implementation_contract"])
        if "provenance" in record:
            provenance = record["provenance"]
            if not isinstance(provenance, dict) or set(provenance) - PROVENANCE_FIELDS:
                raise ValueError("Unknown provenance fields")
            _required(provenance, "repository_github_id", "record_path")
            if type(provenance["repository_github_id"]) is not int:
                raise ValueError("Provenance repository identity must be an integer")
            if any(not isinstance(value, str) for key, value in provenance.items() if key != "repository_github_id"):
                raise ValueError("Provenance metadata must use scalar strings")
            _portable_path(provenance["record_path"])
            owner = repos.get(provenance["repository_github_id"])
            if owner is None or owner["private"]:
                raise ValueError("Source provenance must belong to a public existing owner")
        if kind == "software_system":
            _required(record, "name", "responsibility")
            if "repository_github_id" in record:
                repo = repos.get(record["repository_github_id"])
                if repo is None:
                    raise ValueError("Software refers to an unknown repository")
                expected = "restricted" if repo["private"] else "public"
                if record["visibility"] != expected:
                    raise ValueError("Software visibility differs from its repository")
        elif kind == "capability":
            _required(record, "description")
        elif kind == "module":
            _required(record, "software_ref", "capability_refs", "path", "interfaces")
            if not record["capability_refs"] or not isinstance(record["interfaces"], list):
                raise ValueError("Module needs capabilities and explicit interface list")
        elif kind == "source_media":
            _required(record, "description", "content_digest", "provenance")
            if not re.fullmatch(r"sha256:[a-f0-9]{64}", record["content_digest"]):
                raise ValueError("Source media needs a verified SHA-256 content identity")
            _required(record["provenance"], "original_name")
        elif kind == "composition":
            _required(record, "software_ref", "artwork_ref", "source_media_refs", "status")
        elif kind == "artwork":
            _required(record, "project_id", "title", "publication_status")
            if record["project_id"] not in project_ids or record["project_id"] in artwork_project_ids:
                raise ValueError("Artwork must resolve to one unique existing project")
            artwork_project_ids.add(record["project_id"])
            if record["publication_status"] not in ("unverified", "unpublished", "published"):
                raise ValueError("Invalid artwork publication status")
        elif kind == "edition":
            _required(record, "native_id", "artwork_ref", "composition_ref", "path", "publication_status", "provenance")
            if record["publication_status"] not in ("unverified", "unpublished", "published"):
                raise ValueError("Invalid edition publication status")
            composition = records[record["composition_ref"]["id"]]
            if composition["artwork_ref"] != record["artwork_ref"]:
                raise ValueError("Edition and composition must refer to the same artwork")
            software = records[composition["software_ref"]["id"]]
            if record["provenance"]["repository_github_id"] != software.get("repository_github_id"):
                raise ValueError("Edition provenance differs from composition owner")
        elif kind == "archive":
            _required(record, "description", "legacy_slug")
            if record["legacy_slug"] not in {a["slug"] for a in manifest["archives"]}:
                raise ValueError("Archive must refer to a retained existing archive")
    for group, field in (("repositories", "software_ref"), ("projects", "identity_ref")):
        for item in manifest[group]:
            if field in item:
                expected = "software_system" if group == "repositories" else item[field]["type"]
                if expected not in ("software_system", "artwork"):
                    raise ValueError("Project identity must describe software or artwork")
                _ref(item[field], expected, records)
                if group == "repositories" and records[item[field]["id"]].get("repository_github_id") != item["github_id"]:
                    raise ValueError("Repository/software identity mismatch")
    for group, key in (("repositories", "key"), ("components", "slug"), ("archives", "slug")):
        destinations = {}
        for item in manifest[group]:
            canonical = item.get("directory_slug", item[key])
            if not ID.fullmatch(canonical):
                raise ValueError("Invalid functional directory slug")
            for value in {canonical, item[key]}:
                if value in destinations and destinations[value] != item[key]:
                    raise ValueError("Canonical directory collides with a compatibility alias")
                destinations[value] = item[key]
    return records


def validate_publication(manifest):
    access = manifest.get("access", {})
    if access.get("repository_id") != 1413700288 or access.get("observed_visibility") != "public":
        raise ValueError("Coordination access observation is missing or changed; recheck publication contract")
    if not access.get("checked_at") or access.get("publication_policy") != "public-existing-relationships-only":
        raise ValueError("Missing conservative publication policy")
    for repo in manifest["repositories"]:
        if type(repo.get("private")) is not bool:
            raise ValueError("Repository privacy must be explicit")
    private = [r for r in manifest["repositories"] if r["private"]]
    if {r["github_id"] for r in private} != LEGACY_PRIVATE_IDS:
        raise ValueError("New or changed private repository relationship requires a publication review")
    keys = {r["key"] for r in private}
    sensitive = {
        "repositories": [{k: v for k, v in r.items() if k not in REPOSITORY_ADDITIONS} for r in private],
        "projects": [{k: v for k, v in p.items() if k not in PROJECT_ADDITIONS}
                     for p in manifest["projects"] if keys.intersection(p["repository_keys"])],
    }
    digest = hashlib.sha256(json.dumps(sensitive, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if digest != LEGACY_PRIVATE_SHA256:
        raise ValueError("Private relationship differs from frozen published baseline")
    # Restricted implementations may be represented by existing repository IDs and
    # functional responsibilities, but private implementation/source manifests may
    # not be copied into this public coordination repository.
    for collection, records in manifest["identity_registry"].items():
        if not isinstance(records, list):
            continue
        for record in records:
            if record["visibility"] == "restricted":
                if collection != "software_systems" or record.get("repository_github_id") not in LEGACY_PRIVATE_IDS:
                    raise ValueError("Private implementation or source records belong in their private owner")
                if set(record) - {"type", "id", "name", "responsibility", "visibility", "repository_github_id"}:
                    raise ValueError("Private software record contains source relationships")
                expected = PRIVATE_SOFTWARE[record["repository_github_id"]]
                owner = next(r for r in private if r["github_id"] == record["repository_github_id"])
                if (record["id"], record["name"]) != expected or record["responsibility"] != owner["role"]:
                    raise ValueError("Private software descriptor differs from reviewed public responsibility")
    records = {r["id"]: r for group in COLLECTIONS for r in manifest["identity_registry"][group]}
    for record in records.values():
        if record["type"] in ("module", "composition"):
            software = records[record["software_ref"]["id"]]
            if software["visibility"] == "restricted":
                raise ValueError("Private module or composition relationship cannot be published")


def validate_manifest(manifest):
    if manifest.get("schema_version") != "2.1.0":
        raise ValueError("Unsupported manifest contract")
    validate_registry(manifest)
    validate_publication(manifest)


def public_catalog(manifest):
    """Return a whitelist projection, never a redaction of arbitrary nested data."""
    validate_manifest(manifest)
    repos = []
    public_keys = set()
    for repo in manifest["repositories"]:
        fields = ("key", "github_id", "private", "directory_slug")
        projected = {k: deepcopy(repo[k]) for k in fields if k in repo}
        if repo["private"]:
            projected["role"] = "Restricted implementation; source relationships are withheld."
        else:
            public_keys.add(repo["key"])
            for key in ("full_name", "role", "software_ref"):
                if key in repo:
                    projected[key] = deepcopy(repo[key])
        repos.append(projected)
    registry = manifest.get("identity_registry", {})
    public_ids = {r["id"] for group in COLLECTIONS for r in registry.get(group, []) if r["visibility"] == "public"}
    projects = []
    for project in manifest["projects"]:
        fields = ("id", "slug", "title", "profile", "aliases")
        item = {k: deepcopy(project[k]) for k in fields}
        if any(key not in public_keys for key in project["repository_keys"]):
            item["aliases"] = []
        item["repository_keys"] = [key for key in project["repository_keys"] if key in public_keys]
        item["repository_subpath"] = project.get("repository_subpath") if item["repository_keys"] else None
        item["local_bindings"] = {}
        if project.get("identity_ref", {}).get("id") in public_ids:
            item["identity_ref"] = deepcopy(project["identity_ref"])
        item["source_state"] = "metadata-only"
        item["decision"] = "Retained project membership. Artwork titles and legacy aliases do not name reusable software."
        projects.append(item)
    result = {"schema_version": manifest["schema_version"], "name": manifest["name"],
              "display_title": manifest["display_title"], "repositories": repos, "projects": projects,
              "components": [], "archives": []}
    for group in ("components", "archives"):
        for item in manifest[group]:
            projected = {k: deepcopy(item[k]) for k in ("slug", "directory_slug", "version_control") if k in item}
            projected["role"] = ("Preserved source; custody details remain in the existing owner."
                                 if group == "archives" else "Existing component; no duplicate implementation is created.")
            result[group].append(projected)
    restricted_projects = {p["id"] for p in manifest["projects"]
                           if any(key not in public_keys for key in p["repository_keys"])}
    if registry:
        result["identity_registry"] = {"schema_version": registry["schema_version"]}
        for group in COLLECTIONS:
            projected_records = []
            for record in registry[group]:
                if record["id"] not in public_ids:
                    continue
                fields = COMMON_FIELDS | ENTITY_FIELDS[record["type"]]
                item = {key: deepcopy(record[key]) for key in sorted(fields) if key in record}
                if record["type"] == "artwork" and record["project_id"] in restricted_projects:
                    item["aliases"] = []
                if "provenance" in item:
                    item["provenance"] = {key: deepcopy(record["provenance"][key])
                                          for key in sorted(PROVENANCE_FIELDS) if key in record["provenance"]}
                projected_records.append(item)
            result["identity_registry"][group] = projected_records
        for records in result["identity_registry"].values():
            if isinstance(records, list):
                for record in records:
                    for key in list(record):
                        if key in REF_TYPES:
                            refs = record[key] if key.endswith("_refs") else [record[key]]
                            if any(ref["id"] not in public_ids for ref in refs):
                                raise ValueError("Public entity references restricted identity")
    return result
