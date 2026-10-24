"""Unit tests for T12: Source-Led Works Material & Continuation Record Registry."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_led_records", TOOLS / "source_led_records.py")
slr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(slr)


class SourceLedRecordsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest_path = slr.default_manifest_path()
        self.manifest_data = json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def test_default_manifest_exists_and_passes_validation(self) -> None:
        self.assertTrue(self.manifest_path.is_file(), f"Missing {self.manifest_path}")
        errors = slr.validate_manifest(self.manifest_path)
        self.assertEqual(errors, [], f"Manifest validation errors: {errors}")

    def test_schema_and_work_counts(self) -> None:
        self.assertEqual(self.manifest_data.get("schema"), slr.SCHEMA)
        works = self.manifest_data.get("works", {})
        self.assertEqual(len(works), 8)
        for name in slr.ALL_SOURCE_LED_WORKS:
            self.assertIn(name, works)
        for name in slr.UNBOUND_WORKS:
            self.assertEqual(works[name]["binding_status"], "unbound")
        self.assertEqual(works["wrvng-v"]["binding_status"], "hybrid")

    def test_backwards_up_hill_denominator(self) -> None:
        buh = self.manifest_data["works"]["backwards-up-hill"]
        denom = buh["denominator"]
        self.assertEqual(denom["total_audio_files"], 94)
        self.assertEqual(denom["track_1_8_files"], 40)
        self.assertEqual(denom["track_1_9_files"], 40)
        self.assertEqual(denom["bounces_masters_files"], 14)
        self.assertEqual(
            denom["track_1_8_files"] + denom["track_1_9_files"] + denom["bounces_masters_files"],
            94,
        )
        self.assertEqual(denom["staged_partial_stems"], 3)
        self.assertFalse(denom["full_bank_complete"])

        # Tampering with full_bank_complete when only 3 stems staged must fail
        tampered = json.loads(json.dumps(self.manifest_data))
        tampered["works"]["backwards-up-hill"]["denominator"]["full_bank_complete"] = True
        errors = slr.validate_denominators(tampered["works"])
        self.assertTrue(any("full_bank_complete must be false" in e for e in errors))

    def test_cycles_denominator(self) -> None:
        cycles = self.manifest_data["works"]["cycles"]
        denom = cycles["denominator"]
        self.assertEqual(denom["primary_originals_count"], 24)
        self.assertEqual(denom["primary_originals_bytes"], 152079224)
        self.assertEqual(denom["backup_overlap_count"], 24)
        self.assertEqual(denom["backup_overlap_bytes"], 152079224)
        self.assertTrue(denom["byte_identical_verified"])

    def test_etc_denominator(self) -> None:
        etc = self.manifest_data["works"]["etc"]
        denom = etc["denominator"]
        self.assertEqual(denom["master_tracks_count"], 4)
        self.assertEqual(denom["master_tracks_bytes"], 174804648)
        self.assertEqual(denom["logic_project_backups_count"], 29)
        self.assertTrue(denom["requires_generation_comparison"])

    def test_noonlight_denominator(self) -> None:
        noon = self.manifest_data["works"]["noonlight"]
        denom = noon["denominator"]
        self.assertEqual(denom["total_assets"], 27)
        self.assertEqual(denom["total_bytes"], 37796913)
        breakdown = denom["asset_breakdown"]
        self.assertEqual(breakdown["dated_png"], 7)
        self.assertEqual(breakdown["numbered_jpg"], 16)
        self.assertEqual(breakdown["mov_studies"], 3)
        self.assertEqual(breakdown["psd_master"], 1)
        self.assertEqual(
            breakdown["dated_png"] + breakdown["numbered_jpg"] + breakdown["mov_studies"] + breakdown["psd_master"],
            27,
        )

    def test_nrcsvs_layer_separation_guard(self) -> None:
        nrcsvs = self.manifest_data["works"]["nrcsvs"]
        self.assertEqual(nrcsvs["layers"], ["narcissus", "echo", "macro-container"])
        self.assertTrue(nrcsvs["layer_separation_enforced"])
        self.assertTrue(nrcsvs["disallow_flat_clip_buckets"])
        self.assertEqual(slr.validate_nrcsvs_layer_separation(nrcsvs), [])

        # Flat clip bucket attack: flat list of clips instead of 3 layers
        flat_record = {
            "layers": ["clip1.mov", "clip2.mov", "clip3.mov"],
            "layer_separation_enforced": True,
            "disallow_flat_clip_buckets": True,
        }
        errors = slr.validate_nrcsvs_layer_separation(flat_record)
        self.assertTrue(any("mismatch" in e for e in errors))

        # Missing layers
        missing_record = {"layers": ["narcissus", "echo"]}
        errors = slr.validate_nrcsvs_layer_separation(missing_record)
        self.assertTrue(any("mismatch" in e for e in errors))

    def test_nvde_lineage_separation_guard(self) -> None:
        nvde = self.manifest_data["works"]["nvde"]
        self.assertEqual(nvde["lineages"], ["nvde-performance-video", "nvde-digital-garden"])
        self.assertTrue(nvde["lineage_separation_enforced"])
        self.assertTrue(nvde["disallow_lineage_conflation"])
        self.assertEqual(slr.validate_nvde_lineage_separation(nvde), [])

        # Conflated lineage attack
        conflated = {
            "lineages": ["nvde-unified-lineage"],
            "lineage_separation_enforced": True,
            "disallow_lineage_conflation": True,
        }
        errors = slr.validate_nvde_lineage_separation(conflated)
        self.assertTrue(any("mismatch" in e for e in errors))

    def test_passing_thru_denominator(self) -> None:
        pt = self.manifest_data["works"]["passing-thru"]
        denom = pt["denominator"]
        self.assertEqual(denom["total_stages"], 7)
        self.assertEqual(denom["total_bytes"], 2422068546)
        expected_stages = [
            "logic_demos",
            "ableton_session",
            "stems",
            "mixdowns",
            "Premiere_ assembly",
            "touchdesigner_pass",
            "final_masters",
        ]
        self.assertEqual(denom["stages"], expected_stages)

    def test_wrvng_v_dual_lineage(self) -> None:
        wrv = self.manifest_data["works"]["wrvng-v"]
        self.assertEqual(wrv["binding_status"], "hybrid")
        self.assertEqual(wrv["bound_implementation_repo"], "4444J99/audiovisual-media-postproduction-system")
        dual = wrv["dual_lineage"]
        self.assertEqual(dual["audio"]["total_bytes"], 220762256)
        self.assertEqual(dual["visual"]["format"], "touchdesigner_toe")

    def test_public_safety_guards(self) -> None:
        # Clean data passes
        self.assertEqual(slr.check_public_safety(self.manifest_data), [])

        # Host path leakage /Users/ rejected
        leak1 = {"path": "/Users/someone/Desktop/media.wav"}
        self.assertTrue(any("/Users/" in e for e in slr.check_public_safety(leak1)))

        # Host path leakage /Volumes/ rejected
        leak2 = {"volume": "/Volumes/ExternalDrive/media.wav"}
        self.assertTrue(any("/Volumes/" in e for e in slr.check_public_safety(leak2)))

        # Control character injection rejected
        ctrl1 = {"note": "malicious\x00injection"}
        self.assertTrue(any("control characters" in e for e in slr.check_public_safety(ctrl1)))
        ctrl2 = {"malicious\x1bkey": "normal_val"}
        self.assertTrue(any("control characters" in e for e in slr.check_public_safety(ctrl2)))

    def test_cli_validate_and_summary(self) -> None:
        # Validate subcommand
        self.assertEqual(slr.main(["validate", "--manifest", str(self.manifest_path)]), 0)

        # Summary subcommand
        buf = io.StringIO()
        with redirect_stdout(buf):
            ret = slr.main(["summary", "--manifest", str(self.manifest_path)])
        self.assertEqual(ret, 0)
        output = buf.getvalue()
        self.assertIn("ACE Source-Led Continuation Records Registry", output)
        self.assertIn("Total Tracked Works: 8", output)
        self.assertIn("backwards-up-hill", output)
        self.assertIn("passing-thru", output)
        self.assertIn("wrvng-v", output)


if __name__ == "__main__":
    unittest.main()
