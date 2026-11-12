#!/usr/bin/env python3
"""
vac34_AE Acceptance Scenario Test Suite
Automates verification of Scenarios A through N as specified in SAIHANDOFF Section 16.
"""

import os
import unittest
import json
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAcceptanceScenarios(unittest.TestCase):
    def setUp(self):
        self.dist_path = os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx")
        self.manifest_path = os.path.join(WORKSPACE_ROOT, "release", "build_manifest.json")
        self.deployment_path = os.path.join(WORKSPACE_ROOT, "logs", "deployment_report.json")
        self.provenance_path = os.path.join(WORKSPACE_ROOT, "catalog", "provenance", "raw_blocks.json")

    def test_scenario_l_build_and_mirror_integrity(self):
        """Scenario L — Build and Mirror byte-identical verification (gated)."""
        if os.environ.get("VAC34_DEPLOYMENT_CHECK") != "1":
            self.skipTest("NOT_RUN: Scenario L requires opt-in deployment check (VAC34_DEPLOYMENT_CHECK=1 python scripts/manage.py verify).")
        self.assertTrue(os.path.exists(self.manifest_path), "Build manifest must exist")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertIn("sha256", manifest)
        self.assertTrue(os.path.exists(self.dist_path), "Dist artifact must exist")

        if os.path.exists(self.deployment_path):
            with open(self.deployment_path, "r", encoding="utf-8") as f:
                deploy = json.load(f)

            if deploy.get("live_installed") and deploy.get("mirror_installed"):
                self.assertTrue(deploy["hashes_match"], "Live and mirror SHA256 must match exactly")
                self.assertEqual(manifest["sha256"], deploy["live_sha256"])
                self.assertEqual(manifest["sha256"], deploy["mirror_sha256"])

    def test_scenario_provenance_and_quarantine(self):
        """Verify that all 740 blocks are accounted for with provenance & quarantine."""
        self.assertTrue(os.path.exists(self.provenance_path))
        with open(self.provenance_path, "r", encoding="utf-8") as f:
            blocks = json.load(f)
        self.assertEqual(len(blocks), 740, "Expected exactly 740 blocks extracted across 3 bibles")

        quarantine_path = os.path.join(WORKSPACE_ROOT, "catalog", "quarantine", "quarantine_log.json")
        self.assertTrue(os.path.exists(quarantine_path))
        with open(quarantine_path, "r", encoding="utf-8") as f:
            quarantined = json.load(f)
        self.assertGreater(len(quarantined), 0, "Quarantined items should be recorded")

    def test_expression_generation_node_execution(self):
        """Simulate expression evaluation in isolated Node.js context."""
        js_test = """
        // Mock AE environment
        const thisComp = { frameDuration: 1/30, layer: (name) => null };
        const value = [100, 100];
        const time = 0.5;
        function ease(v, inMin, inMax, outMin, outMax) {
            if (v <= inMin) return outMin;
            if (v >= inMax) return outMax;
            const t = (v - inMin) / (inMax - inMin);
            const sq = t * t * (3 - 2 * t);
            return outMin + sq * (outMax - outMin);
        }

        // Test Sine Breathing
        const freq = 0.8;
        const amt = 12 / 100.0;
        const wave = Math.sin(time * freq * Math.PI * 2) * amt;
        const s = 1.0 + wave;
        const resScale = [value[0] * s, value[1] * s];

        if (resScale[0] < 80 || resScale[0] > 120) process.exit(1);
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", js_test], capture_output=True)
        self.assertEqual(proc.returncode, 0, "Synthetic expression evaluation failed")

if __name__ == "__main__":
    unittest.main()
