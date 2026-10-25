#!/usr/bin/env python3
"""T12: Source-Led Works Material & Continuation Record Registry.

Enforces exact denominator accounting, lineage separation guards, and public safety
controls across all 7 unbound source-led works and hybrid wrvng-v.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "ace.source_led_continuation_records.v1"

UNBOUND_WORKS = (
    "backwards-up-hill",
    "cycles",
    "etc",
    "noonlight",
    "nrcsvs",
    "nvde",
    "passing-thru",
)

ALL_SOURCE_LED_WORKS = UNBOUND_WORKS + ("wrvng-v",)

NRCSVS_REQUIRED_LAYERS = ("narcissus", "echo", "macro-container")
NVDE_REQUIRED_LINEAGES = ("nvde-performance-video", "nvde-digital-garden")

PASSING_THRU_STAGES = (
    "logic_demos",
    "ableton_session",
    "stems",
    "mixdowns",
    "Premiere_ assembly",
    "touchdesigner_pass",
    "final_masters",
)

CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")
FORBIDDEN_PATH_PREFIXES = ("/Users/", "/Volumes/")


def check_public_safety(value: Any, path: str = "root") -> list[str]:
    """Recursively verify that no private machine paths or control characters exist."""
    errors: list[str] = []
    if isinstance(value, str):
        for prefix in FORBIDDEN_PATH_PREFIXES:
            if prefix in value:
                errors.append(f"Public safety violation at '{path}': forbidden path prefix '{prefix}'")
        if CONTROL_CHAR_RE.search(value):
            errors.append(f"Public safety violation at '{path}': unescaped control characters detected")
    elif isinstance(value, dict):
        for k, v in value.items():
            if isinstance(k, str) and CONTROL_CHAR_RE.search(k):
                errors.append(f"Public safety violation at key '{path}.{k}': control characters in key")
            errors.extend(check_public_safety(v, f"{path}.{k}"))
    elif isinstance(value, (list, tuple)):
        for idx, item in enumerate(value):
            errors.extend(check_public_safety(item, f"{path}[{idx}]"))
    return errors


def validate_nrcsvs_layer_separation(record_or_layers: Any) -> list[str]:
    """Verify that NRCSVS enforces discrete 3-layer architecture and disallows flat clip buckets."""
    errors: list[str] = []
    layers = (
        record_or_layers.get("layers")
        if isinstance(record_or_layers, dict)
        else record_or_layers
    )
    if not isinstance(layers, (list, tuple)):
        return ["NRCSVS must declare a structured 'layers' sequence (flat clip buckets disallowed)"]
    if len(layers) != len(NRCSVS_REQUIRED_LAYERS) or tuple(layers) != NRCSVS_REQUIRED_LAYERS:
        errors.append(
            f"NRCSVS layer architecture mismatch: expected exactly {list(NRCSVS_REQUIRED_LAYERS)}, got {list(layers)}"
        )
    if isinstance(record_or_layers, dict):
        if not record_or_layers.get("layer_separation_enforced"):
            errors.append("NRCSVS record must assert 'layer_separation_enforced: true'")
        if not record_or_layers.get("disallow_flat_clip_buckets"):
            errors.append("NRCSVS record must assert 'disallow_flat_clip_buckets: true'")
    return errors


def validate_nvde_lineage_separation(record_or_lineages: Any) -> list[str]:
    """Verify that NVDE enforces discrete 2-lineage architecture and disallows conflation."""
    errors: list[str] = []
    lineages = (
        record_or_lineages.get("lineages")
        if isinstance(record_or_lineages, dict)
        else record_or_lineages
    )
    if not isinstance(lineages, (list, tuple)):
        return ["NVDE must declare a structured 'lineages' sequence (conflation disallowed)"]
    if len(lineages) != len(NVDE_REQUIRED_LINEAGES) or tuple(lineages) != NVDE_REQUIRED_LINEAGES:
        errors.append(
            f"NVDE lineage architecture mismatch: expected exactly {list(NVDE_REQUIRED_LINEAGES)}, got {list(lineages)}"
        )
    if isinstance(record_or_lineages, dict):
        if not record_or_lineages.get("lineage_separation_enforced"):
            errors.append("NVDE record must assert 'lineage_separation_enforced: true'")
        if not record_or_lineages.get("disallow_lineage_conflation"):
            errors.append("NVDE record must assert 'disallow_lineage_conflation: true'")
    return errors


def validate_denominators(works: dict[str, Any]) -> list[str]:
    """Validate exact denominator accounting across all source-led works."""
    errors: list[str] = []

    # 1. backwards-up-hill: 94 audio files, partial stem subset = 3 -> full_bank_complete: false
    buh = works.get("backwards-up-hill", {})
    buh_denom = buh.get("denominator", {})
    t1_8 = buh_denom.get("track_1_8_files")
    t1_9 = buh_denom.get("track_1_9_files")
    bounces = buh_denom.get("bounces_masters_files")
    total_audio = buh_denom.get("total_audio_files")
    staged_stems = buh_denom.get("staged_partial_stems")
    full_complete = buh_denom.get("full_bank_complete")

    if t1_8 != 40 or t1_9 != 40 or bounces != 14 or total_audio != 94:
        errors.append(
            f"backwards-up-hill denominator error: expected 40 + 40 + 14 = 94 audio files, got {t1_8} + {t1_9} + {bounces} = {total_audio}"
        )
    if staged_stems == 3 and full_complete is not False:
        errors.append(
            "backwards-up-hill: full_bank_complete must be false when only 3 partial stems are staged"
        )

    # 2. cycles: 24 primary originals (152,079,224 bytes), 24 backup overlap (152,079,224 bytes), byte identical
    cycles = works.get("cycles", {})
    cyc_denom = cycles.get("denominator", {})
    if (
        cyc_denom.get("primary_originals_count") != 24
        or cyc_denom.get("primary_originals_bytes") != 152079224
        or cyc_denom.get("backup_overlap_count") != 24
        or cyc_denom.get("backup_overlap_bytes") != 152079224
        or cyc_denom.get("byte_identical_verified") is not True
    ):
        errors.append(
            "cycles denominator error: expected 24 primary / 24 backup overlap (152,079,224 bytes each, byte_identical_verified: true)"
        )

    # 3. etc: 4 master tracks (174,804,648 bytes), 29 logic project backups, requires generation comparison
    etc = works.get("etc", {})
    etc_denom = etc.get("denominator", {})
    if (
        etc_denom.get("master_tracks_count") != 4
        or etc_denom.get("master_tracks_bytes") != 174804648
        or etc_denom.get("logic_project_backups_count") != 29
        or etc_denom.get("requires_generation_comparison") is not True
    ):
        errors.append(
            "etc denominator error: expected 4 master tracks (174,804,648 bytes), 29 logic project backups, and requires_generation_comparison: true"
        )

    # 4. noonlight: 27 assets (37,796,913 bytes: 7 dated PNGs, 16 numbered JPGs, 3 MOV studies, 1 PSD)
    noon = works.get("noonlight", {})
    noon_denom = noon.get("denominator", {})
    breakdown = noon_denom.get("asset_breakdown", {})
    if (
        noon_denom.get("total_assets") != 27
        or noon_denom.get("total_bytes") != 37796913
        or breakdown.get("dated_png") != 7
        or breakdown.get("numbered_jpg") != 16
        or breakdown.get("mov_studies") != 3
        or breakdown.get("psd_master") != 1
    ):
        errors.append(
            "noonlight denominator error: expected 27 assets (37,796,913 bytes: 7 PNG, 16 JPG, 3 MOV, 1 PSD)"
        )

    # 5. nrcsvs: 3 layers
    errors.extend(validate_nrcsvs_layer_separation(works.get("nrcsvs", {})))

    # 6. nvde: 2 lineages
    errors.extend(validate_nvde_lineage_separation(works.get("nvde", {})))

    # 7. passing-thru: 7 stages, 2,422,068,546 bytes
    pt = works.get("passing-thru", {})
    pt_denom = pt.get("denominator", {})
    stages = tuple(pt_denom.get("stages", ()))
    if (
        pt_denom.get("total_stages") != 7
        or pt_denom.get("total_bytes") != 2422068546
        or stages != PASSING_THRU_STAGES
    ):
        errors.append(
            f"passing-thru denominator error: expected 7 stages (2,422,068,546 bytes) matching {list(PASSING_THRU_STAGES)}, got {stages}"
        )

    # 8. wrvng-v: hybrid dual lineage (audio: 220,762,256 bytes, visual TouchDesigner .toe, bound to 4444J99/audiovisual-media-postproduction-system)
    wrv = works.get("wrvng-v", {})
    dual = wrv.get("dual_lineage", {})
    audio = dual.get("audio", {})
    visual = dual.get("visual", {})
    if (
        wrv.get("binding_status") != "hybrid"
        or wrv.get("bound_implementation_repo") != "4444J99/audiovisual-media-postproduction-system"
        or audio.get("total_bytes") != 220762256
        or visual.get("format") != "touchdesigner_toe"
    ):
        errors.append(
            "wrvng-v hybrid lineage error: expected audio 220,762,256 bytes and visual touchdesigner_toe bound to 4444J99/audiovisual-media-postproduction-system"
        )

    return errors


def validate_manifest(manifest_path_or_dict: Path | str | dict[str, Any]) -> list[str]:
    """Validate full source-led continuation records manifest against schema and invariants."""
    errors: list[str] = []
    if isinstance(manifest_path_or_dict, (str, Path)):
        path = Path(manifest_path_or_dict)
        if not path.is_file():
            return [f"Source-led continuation records manifest missing: {path}"]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return [f"Failed to parse source-led continuation records manifest {path}: {exc}"]
    else:
        data = manifest_path_or_dict

    if not isinstance(data, dict):
        return ["Manifest root must be a JSON object"]

    if data.get("schema") != SCHEMA:
        errors.append(f"Invalid schema: expected '{SCHEMA}', got '{data.get('schema')}'")

    works = data.get("works")
    if not isinstance(works, dict):
        return errors + ["Manifest missing 'works' dictionary"]

    for work_name in ALL_SOURCE_LED_WORKS:
        if work_name not in works:
            errors.append(f"Missing required source-led work: '{work_name}'")

    errors.extend(check_public_safety(data))
    errors.extend(validate_denominators(works))
    return errors


def default_manifest_path() -> Path:
    return Path(__file__).resolve().parent.parent / "manifests" / "source-led-continuation-records.json"


def format_summary(data: dict[str, Any]) -> str:
    """Format human-readable summary of source-led continuation records."""
    lines: list[str] = [
        "ACE Source-Led Continuation Records Registry",
        f"Schema: {data.get('schema')}",
        "============================================================",
    ]
    works = data.get("works", {})
    lines.append(f"Total Tracked Works: {len(works)}")
    lines.append(f"Unbound Source-Led Works ({len(UNBOUND_WORKS)}): {', '.join(UNBOUND_WORKS)}")
    lines.append("Hybrid Source-Led Works (1): wrvng-v")
    lines.append("------------------------------------------------------------")

    for name in ALL_SOURCE_LED_WORKS:
        w = works.get(name, {})
        w_type = w.get("work_type", "unknown")
        status = w.get("binding_status", "unknown")
        lines.append(f"• {name} [{w_type} | binding: {status}]:")
        denom = w.get("denominator")
        if denom:
            if "total_audio_files" in denom:
                lines.append(
                    f"    Denominator: {denom.get('total_audio_files')} audio files "
                    f"({denom.get('track_1_8_files')} tracks 1-8, {denom.get('track_1_9_files')} tracks 1-9, "
                    f"{denom.get('bounces_masters_files')} bounces/masters). "
                    f"Staged stems: {denom.get('staged_partial_stems')} (full_bank_complete: {denom.get('full_bank_complete')})"
                )
            elif "primary_originals_count" in denom:
                lines.append(
                    f"    Denominator: {denom.get('primary_originals_count')} primary originals "
                    f"({denom.get('primary_originals_bytes'):,} bytes) == "
                    f"{denom.get('backup_overlap_count')} backup overlap ({denom.get('backup_overlap_bytes'):,} bytes). "
                    f"Byte-identical: {denom.get('byte_identical_verified')}"
                )
            elif "master_tracks_count" in denom:
                lines.append(
                    f"    Denominator: {denom.get('master_tracks_count')} master tracks "
                    f"({denom.get('master_tracks_bytes'):,} bytes), "
                    f"{denom.get('logic_project_backups_count')} logic project backups. "
                    f"Generational comparison required: {denom.get('requires_generation_comparison')}"
                )
            elif "total_assets" in denom:
                b = denom.get("asset_breakdown", {})
                lines.append(
                    f"    Denominator: {denom.get('total_assets')} assets ({denom.get('total_bytes'):,} bytes) "
                    f"[{b.get('dated_png')} PNG, {b.get('numbered_jpg')} JPG, {b.get('mov_studies')} MOV, {b.get('psd_master')} PSD]"
                )
            elif "total_stages" in denom:
                lines.append(
                    f"    Denominator: {denom.get('total_stages')} compositional stages ({denom.get('total_bytes'):,} bytes) "
                    f"-> {', '.join(denom.get('stages', []))}"
                )
        if "layers" in w:
            lines.append(
                f"    Layers (3-layer discrete separation): {', '.join(w.get('layers', []))} "
                f"(flat clip buckets disallowed)"
            )
        if "lineages" in w:
            lines.append(
                f"    Lineages (2-lineage discrete separation): {', '.join(w.get('lineages', []))} "
                f"(conflation disallowed)"
            )
        if "dual_lineage" in w:
            dl = w["dual_lineage"]
            audio_bytes = dl.get("audio", {}).get("total_bytes", 0)
            vis_fmt = dl.get("visual", {}).get("format")
            repo = w.get("bound_implementation_repo")
            lines.append(
                f"    Dual Lineage: audio ({audio_bytes:,} bytes) + visual ({vis_fmt}) bound to {repo}"
            )
        custody = w.get("custody_requirement")
        if custody:
            lines.append(f"    Custody Rule: {custody}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--manifest",
        type=Path,
        default=default_manifest_path(),
        help="Path to source-led continuation records manifest",
    )

    parser = argparse.ArgumentParser(
        description="ACE Source-Led Works Material & Continuation Record Registry",
        parents=[common_parser],
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "validate",
        parents=[common_parser],
        help="Validate source-led records against schema and invariants",
    )
    subparsers.add_parser(
        "summary",
        parents=[common_parser],
        help="Print structured summary of all 8 source-led works",
    )

    args = parser.parse_args(argv)

    if not args.command or args.command == "validate":
        errors = validate_manifest(args.manifest)
        if errors:
            print(f"FAIL: Source-led continuation records validation errors in {args.manifest}:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        print(f"PASS: Source-led continuation records verified (8 works, 0 errors) from {args.manifest}")
        return 0

    if args.command == "summary":
        if not args.manifest.is_file():
            print(f"FAIL: Manifest not found: {args.manifest}", file=sys.stderr)
            return 1
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        print(format_summary(data))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
