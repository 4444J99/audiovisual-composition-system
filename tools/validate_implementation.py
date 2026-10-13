#!/usr/bin/env python3
"""Validate an implementation-local ACE contract without importing its runtime."""

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys


KINDS = ("capabilities", "modules", "source_media", "compositions", "artworks", "editions", "archives")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs)


def validate(data, root=None):
    if data.get("schema_version") != "1.0.0" or data.get("system_id") != "audiovisual-composition-system":
        raise ValueError("Unsupported implementation contract")
    repository = data.get("repository", {})
    if type(repository.get("github_id")) is not int or repository["github_id"] <= 0:
        raise ValueError("Repository requires a stable numeric github_id")
    software = data.get("software", {})
    for field in ("id", "name", "responsibility"):
        if not isinstance(software.get(field), str) or not software[field].strip():
            raise ValueError(f"Software requires {field}")
    if not SLUG.fullmatch(software["id"]):
        raise ValueError("Software ID must be a functional portable slug")
    indexed = {}
    for kind in KINDS:
        records = data.get(kind)
        if not isinstance(records, list):
            raise ValueError(f"Missing typed collection: {kind}")
        indexed[kind] = {}
        for item in records:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
                raise ValueError(f"Invalid {kind} identity")
            if item["id"] in indexed[kind]:
                raise ValueError(f"Duplicate {kind} identity")
            indexed[kind][item["id"]] = item
            if "path" in item:
                value = item["path"]
                if not isinstance(value, str) or not value or "\\" in value:
                    raise ValueError("Invalid repository-local path")
                path = PurePosixPath(value)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Repository-local path escapes its owner")
                if root is not None:
                    owner = Path(root).resolve()
                    target = (owner / path).resolve()
                    if not target.is_relative_to(owner) or not target.exists():
                        raise ValueError(f"Unresolved repository-local path: {kind}/{item['id']}")
                    if "json_pointer" in item:
                        current = load_json(target)
                        pointer = item["json_pointer"]
                        if not isinstance(pointer, str) or not pointer.startswith("/"):
                            raise ValueError("Invalid JSON pointer")
                        try:
                            for segment in pointer[1:].split("/"):
                                key = segment.replace("~1", "/").replace("~0", "~")
                                current = current[int(key)] if isinstance(current, list) else current[key]
                        except (KeyError, IndexError, ValueError, TypeError):
                            raise ValueError("Unresolved JSON pointer") from None

    def ref(kind, value):
        if not isinstance(value, str) or value not in indexed[kind]:
            raise ValueError(f"Unresolved typed reference to {kind}")

    for module in data["modules"]:
        if not isinstance(module.get("capability_ids"), list) or not module["capability_ids"]:
            raise ValueError("Module requires capability_ids")
        if not isinstance(module.get("interfaces"), list):
            raise ValueError("Module requires an interfaces array")
        for capability in module["capability_ids"]:
            ref("capabilities", capability)
    for composition in data["compositions"]:
        if "artwork_id" in composition:
            ref("artworks", composition["artwork_id"])
        for field, kind in (("source_media_ids", "source_media"), ("module_ids", "modules")):
            for value in composition.get(field, []):
                ref(kind, value)
    for edition in data["editions"]:
        if "composition_id" not in edition:
            raise ValueError("Edition requires composition_id")
        ref("compositions", edition["composition_id"])
    for artwork in data["artworks"]:
        if not isinstance(artwork.get("title"), str) or not artwork["title"].strip():
            raise ValueError("Artwork requires title metadata")
        if artwork.get("publication_status") not in ("unverified", "unpublished", "published", "draft", "historical"):
            raise ValueError("Artwork requires explicit publication_status")
        labels = [artwork["title"], *artwork.get("aliases", [])]
        if software["id"].casefold() in {label.casefold() for label in labels}:
            raise ValueError("Software ID is an artwork title or alias")
    for source in data["source_media"]:
        if not isinstance(source.get("description"), str) or not source["description"].strip():
            raise ValueError("Source media requires a literal description")
    return {"repository_id": repository["github_id"], "software_id": software["id"], "counts": {kind: len(data[kind]) for kind in KINDS}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="+", type=Path)
    parser.add_argument("--metadata-only", action="store_true", help="Validate types and references without asserting local files exist")
    args = parser.parse_args(argv)
    try:
        for path in args.manifests:
            result = validate(load_json(path), None if args.metadata_only else path.parent)
            result["path_validation"] = not args.metadata_only
            print(json.dumps(result, sort_keys=True))
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f"Implementation contract failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
