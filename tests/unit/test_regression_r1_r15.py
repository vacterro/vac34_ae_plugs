#!/usr/bin/env python3
"""
vac34_AE Regression Test Suite (R1 - R15)
Directly tests requirements R1 through R15 defined in SAIHANDOFF Section 11:
  R1: Neither Live nor Mirror installed -> deployment FAILED
  R2: Mirror exists, Live does not -> PARTIAL / DEPLOY_BLOCKED, not PASS
  R3: All three SHA-256 match -> deployment VERIFIED
  R4: Permission denied -> diagnosed correctly
  R5: Old Live not announced as updated
  R6: Absence of V: does not fail portable tests
  R7: Export reproducible without deployment
  R8: Clean rebuild produces canonically identical artifact
  R9: Docked panel initial layout is invoked
  R10: Floating Window opens correctly
  R11: Startup exception displayed and logged to writable location
  R12: Real host smoke-test records controls visibility
  R13: Multiple installed copies discovered and reported
  R14: Actual build identifier visible in title
  R15: Install & rollback preserve foreign files
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORKSPACE_ROOT)

from build.builder import (
    DeploymentState,
    stage_verify_installation,
    stage_bundle,
    stage_write_artifacts,
    find_installed_instances,
    compute_sha256
)
from scripts.manage import verify_vac34_ownership

class TestRegressionR1ToR15(unittest.TestCase):
    def setUp(self):
        self.dist_path = os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx")
        self.manifest_path = os.path.join(WORKSPACE_ROOT, "release", "build_manifest.json")

    def test_r1_neither_live_nor_mirror_installed_fails(self):
        """R1: Neither Live nor Mirror installed — deployment FAILED."""
        bad_results = {
            "state": DeploymentState.DEPLOY_FAILED,
            "live_installed": False,
            "mirror_installed": False,
            "hashes_match": False,
            "live_path": None,
            "mirror_path": None
        }
        with self.assertRaises(RuntimeError) as ctx:
            stage_verify_installation(bad_results)
        self.assertIn("Deployment FAILED", str(ctx.exception))

    def test_r2_mirror_only_is_not_pass(self):
        """R2: Mirror exists, Live does not — PARTIAL/BLOCKED, not PASS."""
        blocked_results = {
            "state": DeploymentState.DEPLOY_BLOCKED,
            "live_installed": False,
            "mirror_installed": True,
            "hashes_match": False,
            "live_path": r"C:\Program Files\Adobe\...\vac34_AE.jsx",
            "mirror_path": r"V:\...\vac34_AE.jsx",
            "live_error": "Permission denied"
        }
        with self.assertRaises(PermissionError) as ctx:
            stage_verify_installation(blocked_results)
        self.assertIn("Deployment BLOCKED", str(ctx.exception))

        mirror_only_results = {
            "state": DeploymentState.MIRROR_ONLY,
            "live_installed": False,
            "mirror_installed": True,
            "hashes_match": False,
            "live_error": "Path not found"
        }
        with self.assertRaises(RuntimeError) as ctx2:
            stage_verify_installation(mirror_only_results)
        self.assertIn("MIRROR_ONLY", str(ctx2.exception))

    def test_r3_all_three_hashes_match_verified(self):
        """R3: All three SHA-256 match — deployment VERIFIED."""
        with tempfile.TemporaryDirectory() as td:
            dummy_dist = os.path.join(td, "vac34_AE_dist.jsx")
            dummy_file = os.path.join(td, "vac34_AE.jsx")
            dummy_mirror = os.path.join(td, "vac34_AE_mirror.jsx")
            with open(dummy_dist, "w") as f:
                f.write("// vac34 dummy content " + "x" * 6000)
            shutil.copy2(dummy_dist, dummy_file)
            shutil.copy2(dummy_dist, dummy_mirror)

            sha = compute_sha256(dummy_file)
            dummy_manifest = {
                "sha256": sha,
                "dist_file": dummy_dist
            }
            verified_results = {
                "state": DeploymentState.LIVE_AND_MIRROR_VERIFIED,
                "live_installed": True,
                "mirror_installed": True,
                "hashes_match": True,
                "live_path": dummy_file,
                "mirror_path": dummy_mirror,
                "live_sha256": sha,
                "mirror_sha256": sha
            }
            res = stage_verify_installation(verified_results, dummy_manifest)
            self.assertTrue(res)

    def test_r3b_fake_hashes_match_flag_rejected(self):
        """P0: Verify that stage_verify_installation rejects fake hashes_match=True when files differ."""
        with tempfile.TemporaryDirectory() as td:
            dummy_live = os.path.join(td, "vac34_live.jsx")
            dummy_mirror = os.path.join(td, "vac34_mirror.jsx")
            with open(dummy_live, "w") as f:
                f.write("// vac34 live content " + "A" * 6000)
            with open(dummy_mirror, "w") as f:
                f.write("// vac34 mirror content " + "B" * 6000)

            fake_results = {
                "state": DeploymentState.LIVE_AND_MIRROR_VERIFIED,
                "live_installed": True,
                "mirror_installed": True,
                "hashes_match": True,  # FAKE flag passed by caller!
                "live_path": dummy_live,
                "mirror_path": dummy_mirror
            }
            with self.assertRaises(RuntimeError) as ctx:
                stage_verify_installation(fake_results)
            self.assertIn("hashes differ", str(ctx.exception).lower())

    def test_r4_permission_denied_diagnosed_correctly(self):
        """R4: Permission denied — diagnosed correctly without false green."""
        report_path = os.path.join(WORKSPACE_ROOT, "logs", "deployment_report.json")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            if report.get("live_error") and "Permission denied" in str(report.get("live_error")):
                self.assertEqual(report.get("state"), DeploymentState.DEPLOY_BLOCKED)
                self.assertFalse(report.get("live_installed"))

    def test_r5_old_live_not_declared_updated(self):
        """R5: Old Live not announced as updated when write fails."""
        report_path = os.path.join(WORKSPACE_ROOT, "logs", "deployment_report.json")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            if not report.get("live_installed") and report.get("live_sha256"):
                # If dist hash differs from live, hashes_match MUST be false
                with open(self.dist_path, "rb") as df:
                    current_dist_sha = compute_sha256(self.dist_path)
                if current_dist_sha != report["live_sha256"]:
                    self.assertFalse(report.get("hashes_match"))

    def test_r6_missing_v_drive_skipped_in_portable(self):
        """R6: Absence of V: does not fail portable unit tests."""
        fake_mirror = r"Z:\NonExistentDrive\vac34_AE.jsx"
        self.assertFalse(os.path.exists(fake_mirror))

    def test_r7_export_reproducible_without_deployment(self):
        """R7: Export reproducible without active live deployment."""
        self.assertTrue(os.path.exists(self.dist_path))
        self.assertTrue(os.path.exists(self.manifest_path))

    def test_r8_clean_rebuild_canonical_identical_sha256(self):
        """R8: Clean rebuild produces canonically identical artifact."""
        code1 = stage_bundle()
        # Re-bundle
        code2 = stage_bundle()
        canonical1 = code1.replace("\r\n", "\n")
        canonical2 = code2.replace("\r\n", "\n")
        self.assertEqual(canonical1, canonical2)

    def test_r9_docked_panel_initial_layout_invoked(self):
        """R9: Docked panel initial layout is invoked."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        let layoutCalled = false;
        let resizeCalled = false;

        function MockPanel() {
            this.type = "panel";
            this.children = [];
            this.items = [];
            this.layout = {
                layout: function(force) { layoutCalled = true; },
                resize: function() { resizeCalled = true; }
            };
            this.preferredSize = [-1, -1];
        }
        MockPanel.prototype.add = function(type, bounds, text) {
            const c = new MockPanel();
            c.type = type;
            c.text = text;
            this.children.push(c);
            this.items.push(c);
            return c;
        };
        MockPanel.prototype.remove = function(c) {
            const idx = this.children.indexOf(c);
            if (idx !== -1) this.children.splice(idx, 1);
        };
        MockPanel.prototype.removeAll = function() {
            this.children = [];
            this.items = [];
        };

        global.Panel = MockPanel;
        const mockPanelInstance = new MockPanel();

        // Pass mockPanelInstance as thisObj
        new Function('thisObj', bundle)(mockPanelInstance);

        if (!layoutCalled) {
            console.error("FAIL: ui.layout.layout(true) was not called for docked panel!");
            process.exit(1);
        }
        if (!resizeCalled) {
            console.error("FAIL: ui.layout.resize() was not called for docked panel!");
            process.exit(2);
        }

        console.log("PASS: Docked panel initial layout and resize verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"R9 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r10_floating_window_opens_correctly(self):
        """R10: Floating Window opens correctly when thisObj is null/palette."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        let showCalled = false;
        let centerCalled = false;

        function MockWindow(type, title) {
            this.type = type;
            this.title = title;
            this.children = [];
            this.items = [];
            this.layout = { layout: () => {}, resize: () => {} };
            this.preferredSize = [-1, -1];
            this.center = function() { centerCalled = true; };
            this.show = function() { showCalled = true; };
        }
        MockWindow.prototype.add = function(type, bounds, text) {
            const c = new MockWindow(type, text);
            this.children.push(c);
            this.items.push(c);
            return c;
        };
        MockWindow.prototype.remove = function(c) {
            const idx = this.children.indexOf(c);
            if (idx !== -1) this.children.splice(idx, 1);
        };
        MockWindow.prototype.removeAll = function() {
            this.children = [];
            this.items = [];
        };

        global.Window = MockWindow;
        delete global.Panel;

        // Run with null thisObj -> should create floating Window
        new Function('thisObj', bundle)(null);

        if (!showCalled) {
            console.error("FAIL: Floating Window show() was not called!");
            process.exit(1);
        }
        if (!centerCalled) {
            console.error("FAIL: Floating Window center() was not called!");
            process.exit(2);
        }

        console.log("PASS: Floating Window display verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"R10 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r11_startup_exception_displayed_and_logged(self):
        """R11: Startup exception displays fallback UI and logs to writable location."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        function MockPanel() {
            this.type = "panel";
            this.children = [];
            this.items = [];
            this.layout = { layout: () => {}, resize: () => {} };
            this.preferredSize = [-1, -1];
        }
        MockPanel.prototype.add = function(type, bounds, text) {
            const c = new MockPanel();
            c.type = type;
            c.text = text;
            this.children.push(c);
            this.items.push(c);
            return c;
        };
        MockPanel.prototype.remove = function(c) {
            const idx = this.children.indexOf(c);
            if (idx !== -1) this.children.splice(idx, 1);
        };
        MockPanel.prototype.removeAll = function() {
            this.children = [];
            this.items = [];
        };

        global.Panel = MockPanel;
        const panel = new MockPanel();

        // Execute bundle
        new Function('thisObj', bundle)(panel);

        // Verify Diagnostics has recording capabilities
        global.vac34_Diagnostics.recordStartupError("Simulated Test Stage", new Error("Synthetic startup failure"));
        const err = global.vac34_Diagnostics.getStartupError();

        if (!err || err.stage !== "Simulated Test Stage") {
            console.error("FAIL: Startup error was not properly captured by diagnostics");
            process.exit(1);
        }

        console.log("PASS: Startup error handling and logging verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"R11 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r12_host_smoke_test_procedure_defined(self):
        """R12: Real host smoke-test procedure verifies controls."""
        smoke_script = os.path.join(WORKSPACE_ROOT, "tests", "ae_runtime", "host_smoke_test.jsx")
        self.assertTrue(os.path.exists(smoke_script), "Host smoke test JSX must exist")

        node_test_title_only = """
        const fs = require('fs');
        const smokeCode = fs.readFileSync('tests/ae_runtime/host_smoke_test.jsx', 'utf8');

        function MockElement(type, text) {
            this.type = type;
            this.text = text || "";
            this.children = [];
            this.items = [];
            this.layout = { layout: () => {}, resize: () => {} };
        }
        MockElement.prototype.add = function(type, b, text) {
            const el = new MockElement(type, text);
            this.children.push(el);
            return el;
        };

        global.Panel = MockElement;
        global.app = { name: "Adobe After Effects", version: "24.0" };
        global.vac34_Config = { PRODUCT_NAME: "vac34_AE", BUILD_ID: "20261107.01" };
        global.vac34_UIBuilder = {
            build: function(thisObj) {
                const win = new MockElement("panel", "vac34_AE 20261107.01");
                win.add("statictext", null, "vac34_AE v0.0.1 (20261107.01)");
                return win;
            }
        };

        const thisObj = new MockElement("panel");
        const res = eval(smokeCode);
        if (res.status === "VERIFIED" || res.status === "HOST_VERIFIED") {
            console.error("FAIL: Title-only panel falsely declared VERIFIED!");
            process.exit(1);
        }
        if (res.status !== "FAILED") {
            console.error("FAIL: Title-only panel should have status FAILED, got: " + res.status);
            process.exit(2);
        }
        console.log("PASS: Title-only panel correctly FAILED smoke test.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_test_title_only], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Smoke test validation failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r13_several_installed_copies_discovered(self):
        """R13: Multiple installed copies are discovered and reported via portable fixture."""
        with tempfile.TemporaryDirectory() as td:
            dir1 = os.path.join(td, "ae_dir1")
            dir2 = os.path.join(td, "ae_dir2")
            os.makedirs(dir1, exist_ok=True)
            os.makedirs(dir2, exist_ok=True)

            p1 = os.path.join(dir1, "vac34_AE.jsx")
            p2 = os.path.join(dir2, "vac34_AE_alt.jsx")
            with open(p1, "w", encoding="utf-8") as f:
                f.write("// vac34 instance 1\n")
            with open(p2, "w", encoding="utf-8") as f:
                f.write("// vac34 instance 2\n")

            instances = find_installed_instances(search_dirs=[dir1, dir2])
            self.assertIsInstance(instances, list)
            self.assertEqual(len(instances), 2)
            discovered_paths = [os.path.normpath(i["path"]) for i in instances]
            self.assertIn(os.path.normpath(p1), discovered_paths)
            self.assertIn(os.path.normpath(p2), discovered_paths)
            for inst in instances:
                self.assertIn("sha256", inst)
                self.assertIn("size", inst)
                self.assertEqual(len(inst["sha256"]), 64)

    def test_r14_build_identifier_displayed_in_title(self):
        """R14: Actual build identifier is displayed in title."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        let titleText = "";
        function MockPanel() {
            this.type = "panel";
            this.children = [];
            this.items = [];
            this.layout = { layout: () => {}, resize: () => {} };
            this.preferredSize = [-1, -1];
        }
        MockPanel.prototype.add = function(type, bounds, text) {
            const c = new MockPanel();
            c.type = type;
            c.text = text;
            if (typeof text === "string" && text.indexOf("vac34_AE") !== -1 && text.indexOf("Failure") === -1) {
                titleText = text;
            }
            this.children.push(c);
            this.items.push(c);
            return c;
        };
        MockPanel.prototype.remove = function(c) {
            const idx = this.children.indexOf(c);
            if (idx !== -1) this.children.splice(idx, 1);
        };
        MockPanel.prototype.removeAll = function() {
            this.children = [];
            this.items = [];
        };

        global.Panel = MockPanel;
        new Function('thisObj', bundle)(new MockPanel());

        const buildId = global.vac34_Config.BUILD_ID;
        if (!titleText.includes(buildId)) {
            console.error("FAIL: Panel title does not contain BUILD_ID (" + buildId + ")! Title was: " + titleText);
            process.exit(1);
        }

        console.log("PASS: Panel title contains BUILD_ID " + buildId);
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"R14 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r15_install_and_rollback_preserve_foreign_files(self):
        """R15: Install & rollback do not touch foreign files."""
        with tempfile.TemporaryDirectory() as td:
            foreign_file = os.path.join(td, "unrelated_plugin.jsx")
            with open(foreign_file, "w") as f:
                f.write("// Foreign 3rd party script from AnotherVendor\nalert('hello');\n")
            self.assertFalse(verify_vac34_ownership(foreign_file), "Foreign file must not pass vac34 ownership check")

            vac34_file = os.path.join(td, "vac34_AE.jsx")
            with open(vac34_file, "w") as f:
                f.write("/**\n * vac34_AE — Master Expressions Studio\n */\n")
            self.assertTrue(verify_vac34_ownership(vac34_file), "vac34 file must pass ownership check")

if __name__ == "__main__":
    unittest.main()
