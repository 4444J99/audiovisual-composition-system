#!/usr/bin/env python3
"""Fail closed when GitHub identity or visibility differs from the reviewed contract."""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request


def verify_access(manifest, metadata):
    access = manifest["access"]
    actual_id = metadata.get("id")
    if isinstance(actual_id, bool) or str(actual_id) != str(access["repository_id"]):
        raise ValueError("Repository identity differs from reviewed authority")
    visibility = metadata.get("visibility")
    if visibility not in ("public", "private", "internal"):
        raise ValueError("Missing or unknown authenticated repository visibility")
    if visibility != access["observed_visibility"]:
        raise ValueError("Repository visibility changed; review the publication contract before rendering")
    if "private" in metadata and metadata["private"] != (visibility != "public"):
        raise ValueError("Inconsistent repository visibility metadata")
    if metadata.get("archived") is not False:
        raise ValueError("Repository archival state is missing or archived")
    return {"repository_id": access["repository_id"], "visibility": visibility, "verified": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "workspace-manifest.json")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--metadata", type=Path, help="Previously fetched authenticated metadata JSON")
    source.add_argument("--github", action="store_true", help="Read the repository by stable GitHub ID")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text())
        if args.metadata:
            metadata = json.loads(args.metadata.read_text())
        else:
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                raise ValueError("GITHUB_TOKEN is required for authenticated access verification")
            repository_id = manifest["access"]["repository_id"]
            if type(repository_id) is not int or repository_id <= 0:
                raise ValueError("Invalid stable GitHub repository ID")
            request = urllib.request.Request(
                f"https://api.github.com/repositories/{repository_id}",
                headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "User-Agent": "ace-access-verifier"},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                metadata = json.load(response)
        print(json.dumps(verify_access(manifest, metadata), sort_keys=True))
    except (ValueError, KeyError, OSError) as exc:
        print(f"Access verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
