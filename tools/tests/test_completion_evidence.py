"""Coverage and historical override records cannot prove production acceptance."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("completion_layout", ROOT / "tools/workspace_layout.py")
layout = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(layout)


class CompletionEvidenceTests(unittest.TestCase):
    def test_complete_catalog_does_not_grant_estate_readiness(self):
        seal = layout.generate_estate_completion_seal()
        self.assertFalse(seal["ready"])
        self.assertTrue(seal["coverage_ready"])
        self.assertEqual(seal["completion_status"], "not_assessed")
        self.assertEqual(seal["evidence_scope"], "catalog_coverage")
        self.assertTrue(any("source-owner" in error for error in seal["errors"]))

    def test_historical_override_does_not_grant_current_execution(self):
        result = layout.verify_native_admission_status()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["execution_authorized"])
        self.assertEqual(result["current_admission_status"], "not_evaluated")

    def test_unmerged_superseded_pr_cannot_satisfy_baseline(self):
        manifest = json.loads((ROOT / "manifests/project-continuation.json").read_text())
        changed = copy.deepcopy(manifest)
        changed["merged_trunk_baseline"]["generative-multimedia-spatial-environment"]["merged_prs"] = [183, 184, 185]
        result = layout.audit_estate_wave_progression(changed)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("Merged PR mismatch" in error for error in result["errors"]))

    def test_seal_command_fails_closed_without_acceptance(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/workspace_layout.py"), "seal"],
            text=True, capture_output=True, timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        seal = json.loads(result.stdout)
        self.assertFalse(seal["ready"])
        self.assertTrue(seal["coverage_ready"])

    def test_generated_catalog_preserves_historical_admission_boundary(self):
        catalog = layout.rendered_files(layout.load_manifest())["docs/project-catalog.md"]
        self.assertNotIn("external broker waived", catalog)
        self.assertIn("does not grant current execution authority", catalog)


if __name__ == "__main__":
    unittest.main()
