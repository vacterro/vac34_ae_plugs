#!/usr/bin/env python3
"""
vac34_AE Forensic Release Integrity & P0/P1 Regression Test Suite
Covers all 16 regression requirements defined in SAIHANDOFF Section 11:
 1. Rollback preserving reused controllers
 2. Restoring previously changed controller values
 3. Expression failure preserving existing effects
 4. Strict JSON number grammar
 5. Strict JSON string grammar
 6. Serializer availability without native JSON
 7. Audio names with special characters
 8. Initial UI recipe selection
 9. Programmatic preset selection
 10. Shared Master name collisions
 11. Property dimension mismatch
 12. Actual recipe stacking or safe rejection
 13. Full project export coverage
 14. Clean ZIP rebuild
 15. Build manifest verification
 16. Correct deployment and mirror hashes
"""

import os
import sys
import json
import hashlib
import zipfile
import tempfile
import unittest
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def compute_sha256(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

class TestForensicReleaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.dist_path = os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx")
        self.manifest_path = os.path.join(WORKSPACE_ROOT, "release", "build_manifest.json")
        self.mirror_path = r"V:\__STORE_V\_AE\install_AEPlugins\_install_healing\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx"

    def test_01_rollback_preserving_reused_controllers(self):
        """1. Rollback preserving reused controllers."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        let removedEffects = [];

        // Pre-existing controller on the layer
        const existingController = {
            name: "vac34 — Beat Scale Pump — Intensity %",
            matchName: "ADBE Slider Control",
            property: (idx) => ({ value: 35, setValue: () => {} }),
            remove: function() { removedEffects.push(this.name); }
        };

        const unrelatedEffect = {
            name: "Gaussian Blur",
            matchName: "ADBE Gaussian Blur",
            property: (idx) => ({ value: 10, setValue: () => {} }),
            remove: function() { removedEffects.push(this.name); }
        };

        const effectsMap = {
            "vac34 — Beat Scale Pump — Intensity %": existingController,
            "Gaussian Blur": unrelatedEffect
        };

        let addCallCount = 0;
        const mockEffectsGroup = {
            property: (key) => effectsMap[key] || null,
            canAddProperty: (m) => true,
            addProperty: (m) => {
                addCallCount++;
                if (addCallCount >= 1) {
                    // Fail creation of subsequent parameter control
                    return null;
                }
                const eff = {
                    name: "TempNew",
                    matchName: m,
                    property: () => ({ value: 0, setValue: () => {} }),
                    remove: function() { removedEffects.push(this.name); }
                };
                return eff;
            }
        };

        const mockLayer = {
            name: "LayerWithPreexistingControl",
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? mockEffectsGroup : null
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        const res = global.vac34_ControllerManager.setupRecipeControls(mockLayer, recipe, { intensity: 50 });

        if (res !== null) {
            console.error("FAIL: setupRecipeControls should have failed and returned null");
            process.exit(1);
        }

        // P0 Verification: Pre-existing controller and unrelated effects MUST NOT receive remove()
        if (removedEffects.includes("vac34 — Beat Scale Pump — Intensity %")) {
            console.error("P0 VIOLATION: Pre-existing controller was removed during rollback!");
            process.exit(2);
        }

        if (removedEffects.includes("Gaussian Blur")) {
            console.error("P0 VIOLATION: Unrelated user effect was removed during rollback!");
            process.exit(3);
        }

        console.log("PASS: Pre-existing controllers preserved during rollback.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 1 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_02_restoring_previously_changed_controller_values(self):
        """2. Restoring previously changed controller values on rollback."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        let currentValue = 42;
        const existingController = {
            name: "vac34 — Beat Scale Pump — Intensity %",
            matchName: "ADBE Slider Control",
            property: (idx) => ({
                value: currentValue,
                setValue: (v) => { currentValue = v; }
            }),
            remove: () => {}
        };

        const effectsMap = {
            "vac34 — Beat Scale Pump — Intensity %": existingController
        };

        const mockEffectsGroup = {
            property: (key) => effectsMap[key] || null,
            canAddProperty: (m) => true,
            addProperty: (m) => null // Fail on second param
        };

        const mockLayer = {
            name: "LayerWithValues",
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? mockEffectsGroup : null
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        const res = global.vac34_ControllerManager.setupRecipeControls(mockLayer, recipe, { intensity: 99 });

        if (res !== null) {
            console.error("FAIL: setupRecipeControls should have failed");
            process.exit(1);
        }

        // Verify currentValue was restored to 42, not left at 99
        if (currentValue !== 42) {
            console.error("P0 VIOLATION: Controller value was not restored on failure! Current: " + currentValue);
            process.exit(2);
        }

        console.log("PASS: Modified controller values restored on rollback.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 2 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_03_expression_failure_preserving_existing_effects(self):
        """3. Expression failure preserving existing effects."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        global.app = {
            project: { activeItem: null },
            beginUndoGroup: () => {},
            endUndoGroup: () => {}
        };

        let removed = [];
        let curVal = 35;
        const existingController = {
            name: "vac34 — Beat Scale Pump — Intensity %",
            matchName: "ADBE Slider Control",
            property: () => ({
                value: curVal,
                setValue: (v) => { curVal = v; }
            }),
            remove: function() { removed.push(this.name); }
        };

        const effectsGroup = {
            property: (n) => (n === "vac34 — Beat Scale Pump — Intensity %") ? existingController : null,
            canAddProperty: () => true,
            addProperty: (m) => ({
                name: "NewControl",
                matchName: m,
                property: () => ({ value: 0, setValue: () => {} }),
                remove: function() { removed.push(this.name); }
            })
        };

        const targetProp = {
            name: "Scale",
            expression: "",
            canSetExpression: true,
            propertyValueType: 2
        };

        // Make expression assignment throw
        Object.defineProperty(targetProp, "expression", {
            get: () => "",
            set: (v) => { throw new Error("Expression compile failure"); }
        });

        const mockLayer = {
            name: "LayerWithExprFailure",
            selectedProperties: [targetProp],
            property: (p) => {
                if (p === "Transform") return { property: (p2) => (p2 === "Scale" ? targetProp : null) };
                if (p === "Effects" || p === "ADBE Effect Parade") return effectsGroup;
                return null;
            }
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        const res = global.vac34_Engine.applyRecipe(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            recipe,
            { intensity: 80 },
            false
        );

        if (res.ok !== false) {
            console.error("FAIL: applyRecipe should have failed");
            process.exit(1);
        }

        if (removed.includes("vac34 — Beat Scale Pump — Intensity %")) {
            console.error("P0 VIOLATION: Existing controller was removed on expression failure!");
            process.exit(2);
        }

        if (curVal !== 35) {
            console.error("P0 VIOLATION: Existing controller value was not restored! curVal=" + curVal);
            process.exit(3);
        }

        console.log("PASS: Expression failure cleanly rolled back without destroying existing controls.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 3 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_04_strict_json_number_grammar(self):
        """4. Strict JSON number grammar (RFC 8259 conformance)."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const parse = global.vac34_PresetManager.parseJSONStrict;

        // Strictly invalid numbers according to JSON RFC 8259
        const invalidNumbers = [
            '01',
            '-01',
            '00',
            '-001',
            '1.',
            '0.',
            '-5.',
            '1e',
            '1e+',
            '1e-',
            '1.e2',
            '+1',
            '-.5',
            '--1',
            '1.2.3'
        ];

        for (let numStr of invalidNumbers) {
            let threw = false;
            try {
                parse(numStr);
            } catch (e) {
                threw = true;
            }
            if (!threw) {
                console.error("P1 FAIL: parseJSONStrict incorrectly accepted invalid number: " + numStr);
                process.exit(1);
            }
        }

        // Strictly valid numbers
        const validNumbers = [
            '0',
            '-0',
            '123',
            '-456',
            '0.123',
            '-0.005',
            '1e5',
            '1.5e-3',
            '2E+4'
        ];

        for (let numStr of validNumbers) {
            try {
                const res = parse(numStr);
                if (typeof res !== 'number' || !isFinite(res)) {
                    console.error("FAIL: valid number did not parse to finite number: " + numStr);
                    process.exit(2);
                }
            } catch (e) {
                console.error("FAIL: parseJSONStrict threw on valid number: " + numStr + " (" + e.message + ")");
                process.exit(3);
            }
        }

        console.log("PASS: Strict JSON number grammar verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 4 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_05_strict_json_string_grammar(self):
        """5. Strict JSON string grammar, prototype pollution and duplicate key rejection."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const parse = global.vac34_PresetManager.parseJSONStrict;

        const invalidCases = [
            // Raw unescaped literal newline
            '"line1\\nline2"'.replace('\\\\n', '\\n'),
            // Raw unescaped literal carriage return
            '"line1\\rline2"'.replace('\\\\r', '\\r'),
            // Raw unescaped tab
            '"col1\\tcol2"'.replace('\\\\t', '\\t'),
            // Bad escape character
            '"bad escape \\\\a"',
            // Bad unicode escape
            '"bad unicode \\\\u123g"',
            '"short unicode \\\\u12"',
            // Dangerous object keys
            '{"__proto__": {"polluted": true}}',
            '{"constructor": {"prototype": {}}}',
            // Duplicate object key
            '{"key": 1, "key": 2}',
            // Trailing comma
            '{"a": 1,}',
            '[1, 2,]'
        ];

        for (let c of invalidCases) {
            let threw = false;
            try {
                parse(c);
            } catch (e) {
                threw = true;
            }
            if (!threw) {
                console.error("P1 FAIL: parseJSONStrict accepted invalid JSON: " + c);
                process.exit(1);
            }
        }

        console.log("PASS: Strict JSON string grammar & security checks verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 5 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_06_serializer_availability_without_native_json(self):
        """6. Serializer availability without native JSON in runtime."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        // Delete native JSON to simulate ExtendScript CS6 / CC environments without native JSON
        const savedJSON = global.JSON;
        delete global.JSON;

        new Function('thisObj', bundle)(global);

        if (!global.vac34_PresetManager.serializeJSON) {
            console.error("FAIL: serializeJSON not exposed on vac34_PresetManager");
            process.exit(1);
        }

        const testData = {
            product: "vac34_AE",
            version: "0.0.1",
            recipeId: "scale.uniform.breathing",
            masterMode: false,
            parameters: {
                freq: 2.5,
                amt: 15,
                quoted: 'String with "quotes" and \\\\backslashes\\\\ and \\nnewlines'
            },
            arr: [1, 2, -3.14, true, false, null]
        };

        const serialized = global.vac34_PresetManager.serializeJSON(testData);
        if (typeof serialized !== 'string' || serialized.length < 20) {
            console.error("FAIL: serializeJSON produced invalid output: " + serialized);
            process.exit(2);
        }

        // Parse back using strict parser
        const parsed = global.vac34_PresetManager.parseJSONStrict(serialized);
        if (parsed.recipeId !== testData.recipeId || parsed.parameters.freq !== 2.5) {
            console.error("FAIL: Round-trip serialization/deserialization mismatch: " + global.vac34_PresetManager.serializeJSON(parsed));
            process.exit(3);
        }

        // Test savePreset without native JSON
        global.Folder = function() { return { exists: true, create: () => {} }; };
        global.Folder.userData = { fsName: "." };
        let writtenContent = "";
        global.File = function(path) {
            return {
                exists: true,
                open: (mode) => true,
                write: (content) => { writtenContent = content; return true; },
                close: () => {}
            };
        };

        const saved = global.vac34_PresetManager.savePreset("TestPreset", "scale.uniform.breathing", { freq: 3 }, false);
        if (!saved || writtenContent.length === 0) {
            console.error("FAIL: savePreset failed without native JSON");
            process.exit(4);
        }

        console.log("PASS: Serializer operates cleanly without native JSON.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 6 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_07_audio_names_with_special_characters(self):
        """7. Audio layer and channel names with special characters."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const specialAudioNames = [
            'My "Quoted" Audio',
            'Audio with \\\\backslashes\\\\ and "quotes"',
            'Line\\nBreak Audio',
            'Complex "Name" \\'Single\\' & symbols $#@!%^&*()'
        ];

        const specialChannels = [
            'Both "Channels"',
            'Left \\\\Channel\\\\',
            'Right Channel'
        ];

        // Mock AE thisComp environment
        global.thisComp = {
            frameDuration: 1/30,
            layer: (name) => ({
                effect: (cName) => () => ({
                    valueAtTime: (t) => 15
                })
            })
        };
        global.time = 1.0;

        for (let aName of specialAudioNames) {
            for (let cName of specialChannels) {
                const linkCode = global.vac34_AudioEngine.generateAudioLinkCode(aName, cName);
                const envCode = global.vac34_AudioEngine.generateTemporalEnvelopeCode(aName, cName, 2, 10, 5);

                // Verify syntax valid by evaluating in Function
                try {
                    new Function(linkCode)();
                } catch (e) {
                    console.error("P1 FAIL: linkCode syntax error with audio layer '" + aName + "': " + e.message);
                    console.error("Generated code:\\n" + linkCode);
                    process.exit(1);
                }

                try {
                    new Function(envCode)();
                } catch (e) {
                    console.error("P1 FAIL: envCode syntax error with audio layer '" + aName + "': " + e.message);
                    console.error("Generated code:\\n" + envCode);
                    process.exit(2);
                }
            }
        }

        console.log("PASS: Audio layer special characters correctly encoded.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 7 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_08_initial_ui_recipe_selection(self):
        """8. Initial UI recipe selection correctness."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        // Mock ScriptUI environment
        function MockElement(type, text, val) {
            this.type = type;
            this.text = (typeof text === "string") ? text : "";
            this.selection = null;
            this.items = [];
            this.children = [];
            this.enabled = true;
            this.value = (typeof val === "number") ? val : 0;
            this.preferredSize = [100, 20];
            this.add = function(t, bounds, a1, a2, a3) {
                if (t === "item") {
                    const item = { text: a1 || "", index: this.items.length };
                    this.items.push(item);
                    return item;
                }
                const elem = new MockElement(t, (typeof a1 === "string" ? a1 : ""), (typeof a1 === "number" ? a1 : 0));
                this.children.push(elem);
                return elem;
            };
            this.removeAll = function() {
                this.items = [];
            };
            this.remove = function(child) {
                const idx = this.children.indexOf(child);
                if (idx !== -1) this.children.splice(idx, 1);
            };
        }

        global.Window = function(type, title) {
            return new MockElement(type, title);
        };
        global.ScriptUI = {
            newFont: () => ({})
        };

        const win = global.vac34_UIBuilder.build();
        const selected = win.getCurrentSelectedRecipe();

        if (!selected) {
            console.error("P1 FAIL: Initial recipe was not selected automatically!");
            process.exit(1);
        }

        const firstRecipe = global.vac34_RecipeRegistry.getAllRecipes()[0];
        if (selected.id !== firstRecipe.id) {
            console.error("FAIL: Selected recipe is " + selected.id + ", expected " + firstRecipe.id);
            process.exit(2);
        }

        const controlMap = win.getParamControlMap();
        if (selected.parameters && selected.parameters.length > 0) {
            const firstParam = selected.parameters[0];
            if (!controlMap[firstParam.id]) {
                console.error("FAIL: Parameter controls not rendered on initial selection!");
                process.exit(3);
            }
        }

        console.log("PASS: Initial UI selection correctly rendered.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 8 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_09_programmatic_preset_selection(self):
        """9. Programmatic preset selection and value restoration."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        function MockElement(type, text, val) {
            this.type = type;
            this.text = (typeof text === "string") ? text : "";
            this.selection = null;
            this.items = [];
            this.children = [];
            this.enabled = true;
            this.value = (typeof val === "number") ? val : 0;
            this.add = function(t, bounds, a1, a2, a3) {
                if (t === "item") {
                    const item = { text: a1 || "", index: this.items.length };
                    this.items.push(item);
                    return item;
                }
                const elem = new MockElement(t, (typeof a1 === "string" ? a1 : ""), (typeof a1 === "number" ? a1 : 0));
                this.children.push(elem);
                return elem;
            };
            this.removeAll = function() { this.items = []; };
            this.remove = function(child) {
                const idx = this.children.indexOf(child);
                if (idx !== -1) this.children.splice(idx, 1);
            };
        }

        global.Window = function(type, title) { return new MockElement(type, title); };
        global.ScriptUI = { newFont: () => ({}) };

        const win = global.vac34_UIBuilder.build();
        const targetRecipe = global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing");
        const customValues = { freq: 4.5, amount: 28 };

        win.setAuthoritativeSelection(targetRecipe, customValues);

        if (win.getCurrentSelectedRecipe().id !== targetRecipe.id) {
            console.error("FAIL: Authoritative selection did not switch to target recipe");
            process.exit(1);
        }

        const controlMap = win.getParamControlMap();
        if (!controlMap["freq"] || controlMap["freq"].slider.value !== 4.5) {
            console.error("FAIL: Custom preset value freq not set on slider: " + (controlMap["freq"] ? controlMap["freq"].slider.value : "missing"));
            process.exit(2);
        }

        if (controlMap["freq"].editbox.text !== "4.5") {
            console.error("FAIL: Custom preset value freq not set on editbox text");
            process.exit(3);
        }

        console.log("PASS: Programmatic preset selection synchronized correctly.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 9 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_10_shared_master_name_collisions(self):
        """10. Shared Master layer name collisions handled without hijacking foreign user layers."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        // Pre-existing user layer coincidentally named vac34_Master_Controls
        const foreignUserLayer = {
            name: "vac34_Master_Controls",
            comment: "User critical footage layer",
            nullLayer: false,
            guideLayer: false
        };

        const addedLayers = [];
        const mockComp = {
            numLayers: 1,
            layer: (idx) => {
                if (idx === 1) return foreignUserLayer;
                for (let l of addedLayers) {
                    if (l.name === idx) return l;
                }
                return null;
            },
            layers: {
                addNull: () => {
                    const newNull = {
                        name: "TempNull",
                        comment: "",
                        nullLayer: true,
                        guideLayer: true,
                        moveToBeginning: () => {}
                    };
                    addedLayers.push(newNull);
                    return newNull;
                }
            }
        };

        const master = global.vac34_ControllerManager.getOrCreateMasterLayer(mockComp);

        if (master === foreignUserLayer) {
            console.error("P1 VIOLATION: Master controller hijacked foreign user layer!");
            process.exit(1);
        }

        if (foreignUserLayer.comment !== "User critical footage layer") {
            console.error("P1 VIOLATION: Foreign user layer comment was overwritten!");
            process.exit(2);
        }

        if (!master.comment || master.comment.indexOf("vac34_MASTER_LAYER") === -1) {
            console.error("FAIL: Created master layer lacks master identity tag in comment");
            process.exit(3);
        }

        console.log("PASS: Shared master name collision handled safely: " + master.name);
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 10 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_11_property_dimension_mismatch(self):
        """11. Property dimension mismatch rejection (1D, 2D, 3D, Color, Text, separated Position)."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const recipe2D = global.vac34_RecipeRegistry.getRecipeById("position.wiggle.smooth"); // targetDimensions: 2

        // 1D property (e.g. Opacity or Separated X Position)
        const prop1D = {
            name: "X Position",
            expression: "",
            canSetExpression: true,
            propertyValueType: 1
        };

        const layer1D = {
            name: "Layer 1D",
            property: (p) => (p === "Transform" ? { property: () => prop1D } : null)
        };

        const diag1D = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [layer1D] },
            [layer1D],
            recipe2D,
            "Transform.X Position"
        );

        if (diag1D.canApply !== false || diag1D.incompatibleLayers.length !== 1) {
            console.error("P1 FAIL: 2D recipe should be rejected on 1D property!");
            process.exit(1);
        }

        // Color property (dimension 4)
        const propColor = {
            name: "Color",
            expression: "",
            canSetExpression: true,
            propertyValueType: 4
        };
        const layerColor = {
            name: "Layer Color",
            property: (p) => ({ property: () => propColor })
        };
        const diagColor = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [layerColor] },
            [layerColor],
            recipe2D,
            "Effects.Color"
        );
        if (diagColor.canApply !== false) {
            console.error("P1 FAIL: 2D recipe should be rejected on Color property!");
            process.exit(2);
        }

        // Separated Position check
        const propSeparated = {
            name: "Position",
            dimensionsSeparated: true,
            canSetExpression: false,
            propertyValueType: 2
        };
        const layerSep = {
            name: "Layer Sep",
            property: (p) => ({ property: () => propSeparated })
        };
        const diagSep = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [layerSep] },
            [layerSep],
            recipe2D,
            "Transform.Position"
        );
        if (diagSep.canApply !== false) {
            console.error("P1 FAIL: Separated Position main property must be rejected!");
            process.exit(3);
        }

        console.log("PASS: Dimension compatibility checks strictly enforced.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 11 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_12_actual_recipe_stacking_or_safe_rejection(self):
        """12. Cross-recipe stacking safe conflict rejection."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const targetProp = {
            name: "Scale",
            expression: "// [vac34:scale.uniform.breathing]\\nvalue * 1.1;",
            canSetExpression: true,
            propertyValueType: 2
        };

        const mockLayer = {
            name: "LayerWithActiveRecipe",
            selectedProperties: [targetProp],
            property: () => ({ property: () => targetProp })
        };

        const differentRecipe = {
            id: "scale.pop.bounce",
            displayName: "Pop Bounce",
            targetProperties: ["Transform.Scale"],
            targetDimensions: 2,
            parameters: []
        };

        const diag = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            differentRecipe
        );

        if (diag.canApply !== false || diag.conflictedLayers.length !== 1) {
            console.error("FAIL: Differing recipe on same property must be rejected until safe stacking is implemented!");
            process.exit(1);
        }

        console.log("PASS: Cross-recipe conflict rejection verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Test 12 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_13_full_project_export_coverage(self):
        """13. Full project export coverage verification."""
        required = [
            "build/builder.py",
            "build/ingest_bibles.py",
            "dist/vac34_AE.jsx",
            "release/build_manifest.json",
            "release/vac34_AE_v0.0.1.jsx",
            "src/main.js",
            "src/core/Config.js",
            "src/core/Engine.js",
            "src/adapters/AEDom.js",
            "src/adapters/TargetResolver.js",
            "src/controllers/ControllerManager.js",
            "src/audio/AudioEngine.js",
            "src/recipes/RecipeRegistry.js",
            "src/presets/PresetManager.js",
            "src/diagnostics/Diagnostics.js",
            "src/panel/UIBuilder.js",
            "scripts/manage.py",
            "README.md",
            "VERSION"
        ]
        for rel in required:
            full = os.path.join(WORKSPACE_ROOT, rel)
            self.assertTrue(os.path.exists(full), f"Required release file missing: {rel}")

    def test_14_clean_zip_rebuild(self):
        """14. Clean ZIP export and rebuild verification."""
        if os.environ.get("VAC34_EXPORTING") == "1":
            self.skipTest("Skipping nested export during export verification")

        manage_script = os.path.join(WORKSPACE_ROOT, "scripts", "manage.py")
        env = dict(os.environ)
        env["VAC34_EXPORTING"] = "1"
        proc = subprocess.run([sys.executable, manage_script, "export"], cwd=WORKSPACE_ROOT, capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, f"Clean export rebuild failed:\n{proc.stderr}\n{proc.stdout}")
        self.assertIn("Definitive verification complete: PASS", proc.stdout)

    def test_15_build_manifest_verification(self):
        """15. Build manifest verification."""
        self.assertTrue(os.path.exists(self.manifest_path))
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("product"), "vac34_AE")
        self.assertIn("version", manifest)
        self.assertIn("sha256", manifest)
        self.assertIn("source_files", manifest)
        self.assertEqual(manifest["sha256"], compute_sha256(self.dist_path))

    def test_16_correct_deployment_and_mirror_hashes(self):
        """16. Correct deployment and mirror byte-identical hashes (WINDOWS_DEPLOYMENT tier).

        The portable tier only proves the dist hash algorithm against temporary
        fixtures. Physical Live/Mirror equality is a Windows deployment gate,
        opt-in with VAC34_DEPLOYMENT_CHECK=1, and stays byte-strict:
        scripts/manage.py verify re-hashes both real files from disk.
        """
        if os.environ.get("VAC34_DEPLOYMENT_CHECK") != "1":
            self.skipTest("NOT_RUN: physical Live/Mirror hashing is the WINDOWS_DEPLOYMENT tier "
                          "(VAC34_DEPLOYMENT_CHECK=1 python scripts/manage.py verify).")
        dist_sha = compute_sha256(self.dist_path)
        self.assertTrue(len(dist_sha) == 64, "Dist SHA256 must be valid")

        if not os.path.exists(self.mirror_path):
            self.skipTest(f"Windows Backup Mirror not accessible at '{self.mirror_path}'. Skipping deployment check in portable unit suite.")

        mirror_sha = compute_sha256(self.mirror_path)
        self.assertTrue(len(mirror_sha) == 64, "Mirror SHA256 must be valid")
        self.assertEqual(dist_sha, mirror_sha, "Dist and Backup Mirror must be byte-identical")

if __name__ == "__main__":
    unittest.main()
