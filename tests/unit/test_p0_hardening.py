#!/usr/bin/env python3
"""
vac34_AE P0 & P1 Hardening Unit Tests
Directly tests:
  - Foreign expression overwrite protection (byte-identical preservation)
  - Guaranteed Undo Group closure on exception
  - Safe JSON preset validation without code execution
  - 2D vs 3D vector adaptation
"""

import os
import unittest
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestP0Hardening(unittest.TestCase):
    def test_foreign_expression_preservation_mock(self):
        """Regression Test A: Verify that foreign expression is preserved byte-identical."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        // Setup mock environment
        let undoDepth = 0;
        global.app = {
            project: { activeItem: null },
            beginUndoGroup: (n) => { undoDepth++; },
            endUndoGroup: () => { undoDepth--; }
        };

        const targetProp = {
            name: "Position",
            expression: "value + [10, 20]; // User custom foreign expression",
            canSetExpression: true,
            propertyValueType: 2 // 2D_SPATIAL
        };

        const mockLayer = {
            name: "Test Layer",
            selectedProperties: [targetProp],
            property: (p) => {
                if (p === "Transform") return { property: (p2) => (p2 === "Position" ? targetProp : null) };
                if (p === "Effects" || p === "ADBE Effect Parade") return null;
                return null;
            }
        };

        const originalExpr = targetProp.expression;

        // Execute bundle passing global as thisObj
        new Function('thisObj', bundle)(global);

        // Run checkApplication
        const diag = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            global.vac34_RecipeRegistry.getRecipeById("position.wiggle.smooth")
        );

        if (diag.canApply !== false) {
            console.error("FAIL: diag.canApply should be false for foreign expression");
            process.exit(1);
        }

        if (diag.conflictedLayers.length !== 1) {
            console.error("FAIL: foreign expression layer was not recorded in conflictedLayers");
            process.exit(2);
        }

        // Run applyRecipe
        const res = global.vac34_Engine.applyRecipe(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            global.vac34_RecipeRegistry.getRecipeById("position.wiggle.smooth"),
            { freq: 2, amt_x: 20, amt_y: 20 },
            false
        );

        if (targetProp.expression !== originalExpr) {
            console.error("P0 VIOLATION: Foreign expression was modified!");
            process.exit(3);
        }

        if (res.conflictCount !== 1) {
            console.error("FAIL: res.conflictCount should be 1");
            process.exit(4);
        }

        console.log("PASS: Foreign expression preserved byte-identical.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Foreign expression test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_undo_group_closed_on_exception(self):
        """Regression Test B: Guaranteed Undo Group closure on exception."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        let beginCount = 0;
        let endCount = 0;
        global.app = {
            project: { activeItem: null },
            beginUndoGroup: (n) => { beginCount++; },
            endUndoGroup: () => { endCount++; }
        };

        const badLayer = {
            name: "Failing Layer",
            property: () => { throw new Error("Simulated AE DOM crash"); }
        };

        new Function('thisObj', bundle)(global);

        try {
            global.vac34_Engine.applyRecipe(
                { name: "Comp", selectedLayers: [badLayer] },
                [badLayer],
                global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing"),
                {},
                false
            );
        } catch (e) {
            // Expected
        }

        if (global.vac34_AEDom.getUndoDepth() !== 0) {
            console.error("P0 VIOLATION: Undo depth is " + global.vac34_AEDom.getUndoDepth() + " (not closed!)");
            process.exit(1);
        }

        console.log("PASS: Undo group closed cleanly.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Undo group test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_preset_safety_no_arbitrary_code_exec(self):
        """Regression Test H: Ensure presets do not execute arbitrary JavaScript."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        global.codeExecuted = false;
        // Malicious JSON string attempting function execution
        const malicious = '{"recipeId": "scale.uniform.breathing", "evil": (function(){ global.codeExecuted = true; return 1; })()}';

        // Mock File constructor
        global.Folder = function() { return { exists: true, create: () => {} }; };
        global.Folder.userData = { fsName: "." };
        global.File = function() {
            return {
                exists: true,
                open: () => {},
                read: () => malicious,
                close: () => {}
            };
        };

        try {
            global.vac34_PresetManager.loadPreset("malicious_preset");
        } catch (e) {
            // Safe rejection
        }

        if (global.codeExecuted) {
            console.error("P1 SECURITY VIOLATION: Arbitrary code executed during preset load!");
            process.exit(1);
        }

        console.log("PASS: Malicious preset rejected safely.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Preset safety test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_parse_json_strict_direct(self):
        """Regression Test I: Verify pure-JS parseJSONStrict directly parses valid JSON and rejects invalid without eval."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const parse = global.vac34_PresetManager.parseJSONStrict;

        // Valid JSON tests
        const validSamples = [
            '{"recipeId": "position.wiggle.smooth", "parameters": {"freq": 2.5, "amt_x": -10, "enable": true, "text": "hello world"}}',
            '{"arr": [1, 2, -3.14, true, false, null, "item"], "nested": {"k": "v"}}',
            '{}',
            '[]',
            '123.45',
            '"simple string"'
        ];

        for (let s of validSamples) {
            try {
                const parsed = parse(s);
                if (parsed === undefined) {
                    console.error("FAIL: parse returned undefined for valid JSON: " + s);
                    process.exit(1);
                }
            } catch (e) {
                console.error("FAIL: parse threw error on valid JSON: " + s + " -> " + e.message);
                process.exit(2);
            }
        }

        // Invalid JSON tests
        const invalidSamples = [
            '{"trailing": 1} trailing_garbage',
            '{"unclosed": "string',
            '{badKey: 123}',
            '{"val": [1, 2, }',
            'function() { return 1; }',
            'undefined'
        ];

        for (let bad of invalidSamples) {
            let threw = false;
            try {
                parse(bad);
            } catch (e) {
                threw = true;
            }
            if (!threw) {
                console.error("FAIL: parse failed to reject invalid JSON: " + bad);
                process.exit(3);
            }
        }

        console.log("PASS: parseJSONStrict validated.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"parseJSONStrict test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_recipe_conflict_prevention(self):
        """Regression Test J: Prevent cross-recipe conflict overwrite."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        let undoDepth = 0;
        global.app = {
            project: { activeItem: null },
            beginUndoGroup: () => { undoDepth++; },
            endUndoGroup: () => { undoDepth--; }
        };

        const existingExpr = "// [vac34:scale.uniform.breathing]\\n// Parameters: freq=2\\nvalue + [10, 10];";
        const targetProp = {
            name: "Scale",
            expression: existingExpr,
            canSetExpression: true,
            propertyValueType: 2
        };

        const mockLayer = {
            name: "Layer With Breathing",
            selectedProperties: [targetProp],
            property: (p) => {
                if (p === "Transform") return { property: (p2) => (p2 === "Scale" ? targetProp : null) };
                return null;
            }
        };

        // Attempt to check and apply a different recipe to this property
        const recipeA = global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing");
        const recipeB = global.vac34_RecipeRegistry.getRecipeById("position.wiggle.smooth");

        // Verify checkApplication detects conflict if recipe does not match
        // Let's create a recipe that also targets Scale but has different id
        const fakeConflictingRecipe = {
            id: "scale.other.recipe",
            displayName: "Other Scale Recipe",
            targetProperty: "Transform.Scale",
            parameters: []
        };

        const diag = global.vac34_Diagnostics.checkApplication(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            fakeConflictingRecipe
        );

        if (diag.canApply !== false) {
            console.error("FAIL: diag.canApply should be false for conflicting recipe on same property");
            process.exit(1);
        }

        if (diag.conflictedLayers.length !== 1) {
            console.error("FAIL: conflicting layer was not added to conflictedLayers");
            process.exit(2);
        }

        // Now test applyRecipe rejects it
        const res = global.vac34_Engine.applyRecipe(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            fakeConflictingRecipe,
            {},
            false
        );

        if (targetProp.expression !== existingExpr) {
            console.error("FAIL: Existing expression was modified despite conflict!");
            process.exit(3);
        }

        if (res.conflictCount !== 1 || res.appliedCount !== 0) {
            console.error("FAIL: Expected conflictCount: 1, appliedCount: 0; got: " + JSON.stringify(res));
            process.exit(4);
        }

        console.log("PASS: Recipe conflict successfully prevented.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Recipe conflict test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_controller_creation_failure_rollback(self):
        """Regression Test K: Failure during controller creation rolls back and aborts expression assignment."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        global.app = {
            project: { activeItem: null },
            beginUndoGroup: () => {},
            endUndoGroup: () => {}
        };

        const targetProp = {
            name: "Position",
            expression: "",
            canSetExpression: true,
            propertyValueType: 2
        };

        const removedEffects = [];
        const effectsGroup = {
            property: (n) => null,
            canAddProperty: (m) => true,
            addProperty: (m) => {
                // Return an effect, but simulate error on second effect or throw
                return {
                    name: "Effect",
                    property: () => ({ setValue: () => {} }),
                    remove: function() { removedEffects.push(this.name); }
                };
            }
        };

        // Override ensureParameterControl to fail on second parameter
        const origEnsure = global.vac34_ControllerManager.ensureParameterControl;
        let callCount = 0;
        global.vac34_ControllerManager.ensureParameterControl = function(targetLayer, recipe, param) {
            callCount++;
            if (callCount === 2) {
                // Simulate failure on second param
                return null;
            }
            return {
                name: "PartialEffect",
                property: () => ({ setValue: () => {} }),
                remove: function() { removedEffects.push("PartialEffect"); }
            };
        };

        const mockLayer = {
            name: "Layer With Failing Controls",
            selectedProperties: [targetProp],
            property: (p) => {
                if (p === "Transform") return { property: (p2) => (p2 === "Position" ? targetProp : null) };
                if (p === "ADBE Effect Parade" || p === "Effects") return effectsGroup;
                return null;
            }
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("position.wiggle.smooth"); // has freq, amt_x, amt_y

        const res = global.vac34_Engine.applyRecipe(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            recipe,
            { freq: 2, amt_x: 10, amt_y: 10 },
            false
        );

        if (targetProp.expression !== "") {
            console.error("FAIL: Expression was applied despite controller failure!");
            process.exit(1);
        }

        if (res.appliedCount !== 0) {
            console.error("FAIL: appliedCount should be 0; got: " + res.appliedCount);
            process.exit(2);
        }

        if (removedEffects.length !== 1) {
            console.error("FAIL: Partial effects were not rolled back/removed!");
            process.exit(3);
        }

        console.log("PASS: Controller failure cleanly rolled back.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Controller rollback test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p0_setvalue_exception_triggers_transaction_rollback(self):
        """P0 Regression: setValue() throwing exception rolls back transaction, reports exact controller, and aborts Apply."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        global.app = {
            project: { activeItem: null },
            beginUndoGroup: () => {},
            endUndoGroup: () => {}
        };

        const targetProp = {
            name: "Position",
            expression: "",
            canSetExpression: true,
            propertyValueType: 2
        };

        const removedEffects = [];
        let setValueAttempts = [];

        // Pre-existing controller whose setValue will throw
        const failingController = {
            name: "vac34 — Inertial Keyframe Bounce — Bounce Freq",
            matchName: "ADBE Slider Control",
            _vac34Owned: true,
            property: (idx) => ({
                value: 4.0,
                setValue: (v) => {
                    setValueAttempts.push(v);
                    throw new Error("Simulated AE Property Lock: setValue disallowed!");
                }
            }),
            remove: function() { removedEffects.push(this.name); }
        };

        const effectsMap = {
            "vac34 — Inertial Keyframe Bounce — Bounce Freq": failingController
        };

        const mockEffectsGroup = {
            property: (k) => effectsMap[k] || null,
            canAddProperty: (m) => true,
            addProperty: (m) => ({
                name: "NewProp",
                matchName: m,
                property: () => ({ value: 1, setValue: () => {} }),
                remove: function() { removedEffects.push(this.name); }
            })
        };

        const mockLayer = {
            name: "LayerWithFailingSetValue",
            comment: "/* [vac34_rig:physics.spring.inertia] */",
            selectedProperties: [targetProp],
            property: (p) => {
                if (p === "Transform") return { property: (p2) => (p2 === "Position" ? targetProp : null) };
                if (p === "Effects" || p === "ADBE Effect Parade") return mockEffectsGroup;
                return null;
            }
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("physics.spring.inertia");
        const tx = global.vac34_ControllerManager.beginTransaction(mockLayer, recipe);
        const setupSuccess = tx.setup({ freq: 8.5 });

        if (setupSuccess !== false) {
            console.error("P0 VIOLATION: Transaction setup returned true despite setValue() throwing!");
            process.exit(1);
        }

        if (tx.failedOperations.length === 0) {
            console.error("P0 VIOLATION: tx.failedOperations is empty after setValue() error!");
            process.exit(2);
        }

        const failureMsg = tx.failedOperations.join("\\n");
        if (failureMsg.indexOf("Bounce Freq") === -1 && failureMsg.indexOf("setValue") === -1) {
            console.error("P0 VIOLATION: Exact controller name or setValue failure was not recorded: " + failureMsg);
            process.exit(3);
        }

        // Test Engine.applyRecipe behavior when setupRecipeControls fails due to setValue exception
        const applyRes = global.vac34_Engine.applyRecipe(
            { name: "Comp", selectedLayers: [mockLayer] },
            [mockLayer],
            recipe,
            { freq: 8.5 },
            false
        );

        if (applyRes.ok !== false || applyRes.appliedCount !== 0) {
            console.error("P0 VIOLATION: Engine.applyRecipe reported success or appliedCount > 0 when setValue threw!");
            process.exit(4);
        }

        if (targetProp.expression !== "") {
            console.error("P0 VIOLATION: Expression was applied despite setValue failure!");
            process.exit(5);
        }

        console.log("PASS: setValue() exception strictly failed transaction and preserved state.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P0 setValue exception test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p0_foreign_master_null_with_empty_comment_not_hijacked(self):
        """P0 Regression: User null named vac34_Master_Controls with empty comment is NOT hijacked or tagged."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        // Pre-existing user null coincidentally named vac34_Master_Controls with nullLayer=true, guideLayer=true, comment=""
        const foreignNull = {
            name: "vac34_Master_Controls",
            comment: "",
            nullLayer: true,
            guideLayer: true
        };

        const createdLayers = [];
        const mockComp = {
            numLayers: 1,
            layer: (idx) => {
                if (idx === 1 || idx === "vac34_Master_Controls") return foreignNull;
                for (let l of createdLayers) {
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
                        label: 0,
                        moveToBeginning: () => {}
                    };
                    createdLayers.push(newNull);
                    return newNull;
                }
            }
        };

        const master = global.vac34_ControllerManager.getOrCreateMasterLayer(mockComp);

        if (master === foreignNull) {
            console.error("P0 VIOLATION: getOrCreateMasterLayer hijacked user foreign null layer!");
            process.exit(1);
        }

        if (foreignNull.comment !== "") {
            console.error("P0 VIOLATION: foreignNull.comment was stamped with master tag: " + foreignNull.comment);
            process.exit(2);
        }

        if (master.name === "vac34_Master_Controls") {
            console.error("P0 VIOLATION: Newly created master null failed collision avoidance!");
            process.exit(3);
        }

        if (master.comment.indexOf("vac34_MASTER_LAYER_v1") === -1) {
            console.error("P0 VIOLATION: New master lacks master tag");
            process.exit(4);
        }

        console.log("PASS: Foreign user null protected from master hijacking: " + master.name);
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P0 foreign master null test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p0_shared_master_rollback_on_layer_failure(self):
        """P0 Regression: When Shared Master is prepared but all layer applications fail, master controls roll back and empty master null is cleaned up."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        global.app = {
            project: { activeItem: null },
            beginUndoGroup: () => {},
            endUndoGroup: () => {}
        };

        const removedMasterEffects = [];
        let masterLayerRemoved = false;

        const masterEffectsGroup = {
            numProperties: 0,
            property: () => null,
            canAddProperty: () => true,
            addProperty: (m) => {
                masterEffectsGroup.numProperties++;
                return {
                    name: "MasterControl",
                    matchName: m,
                    property: () => ({ value: 10, setValue: () => {} }),
                    remove: function() {
                        masterEffectsGroup.numProperties--;
                        removedMasterEffects.push(this.name);
                    }
                };
            }
        };

        const masterLayer = {
            name: "vac34_Master_Controls",
            comment: "vac34_MASTER_LAYER_v1",
            nullLayer: true,
            guideLayer: true,
            _vac34IsNew: true,
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? masterEffectsGroup : null,
            remove: function() { masterLayerRemoved = true; }
        };

        // Target layer with read-only / failing property
        const posProp = {
            name: "Position",
            canSetExpression: true,
            propertyValueType: 2,
            get expression() { return ""; },
            set expression(v) { throw new Error("Simulated expression syntax/runtime error in AE host!"); }
        };

        const badLayer = {
            name: "FailingLayer",
            selectedProperties: [posProp],
            property: (p) => {
                if (p === "Transform") {
                    return {
                        property: (p2) => (p2 === "Position" ? posProp : null)
                    };
                }
                return null;
            }
        };

        const mockComp = {
            numLayers: 2,
            selectedLayers: [badLayer],
            layer: (i) => (i === 1 ? masterLayer : badLayer)
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("physics.spring.inertia");
        const res = global.vac34_Engine.applyRecipe(mockComp, [badLayer], recipe, { freq: 4 }, true);

        if (res.ok !== false || res.appliedCount !== 0) {
            console.error("FAIL: applyRecipe should have failed completely; got: " + JSON.stringify(res));
            process.exit(1);
        }

        if (removedMasterEffects.length === 0) {
            console.error("P0 VIOLATION: Shared Master controls were NOT rolled back after 100% layer failure!");
            process.exit(2);
        }

        if (!masterLayerRemoved) {
            console.error("P0 VIOLATION: Newly created empty Shared Master layer was not removed on 100% failure!");
            process.exit(3);
        }

        console.log("PASS: Shared Master cleanly rolled back on complete layer failure.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P0 shared master rollback test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p1_foreign_same_name_slider_not_reused_as_owned(self):
        """P1 Regression: Foreign Slider Control with matching name on layer is NOT hijacked or reused as owned."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        let foreignValueModified = false;
        const foreignSlider = {
            name: "vac34 — Sine Breathing Scale — Breathing Speed",
            matchName: "ADBE Slider Control",
            isForeign: true,
            _foreign: true,
            property: () => ({
                value: 999,
                setValue: (v) => { foreignValueModified = true; }
            }),
            remove: () => {}
        };

        const effectsGroup = {
            property: (n) => (n === foreignSlider.name ? foreignSlider : null),
            canAddProperty: () => true,
            addProperty: () => null
        };

        const mockLayer = {
            name: "UserLayerWithForeignSlider",
            comment: "User custom notes — do not touch",
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroup : null
        };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing");
        const param = recipe.parameters[0]; // speed

        const eff = global.vac34_ControllerManager.ensureParameterControl(mockLayer, recipe, param);
        if (eff !== null) {
            console.error("P1 VIOLATION: ensureParameterControl hijacked foreign slider control!");
            process.exit(1);
        }

        const tx = global.vac34_ControllerManager.beginTransaction(mockLayer, recipe);
        const ok = tx.setup({ speed: 2 });
        if (ok !== false) {
            console.error("P1 VIOLATION: Transaction setup succeeded despite foreign control collision!");
            process.exit(2);
        }

        if (foreignValueModified) {
            console.error("P1 VIOLATION: Foreign slider value was modified!");
            process.exit(3);
        }

        console.log("PASS: Foreign slider control protected from reuse.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P1 foreign slider test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p1_audio_escaping_quotes_and_special_chars(self):
        """P1 Regression: Audio source and channel names with quotes, backslashes, and special characters generate valid JavaScript."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const complexAudioName = 'Audio "Master" \\\\ Track #1 [48kHz]';
        const complexChannelName = 'Left "Channel" & \\\\ Peak \\'Strobe\\'';

        const mockLayer = {
            name: "VisualizerLayer",
            threeDLayer: false
        };

        const audioRecipes = [
            "audio.scale.pump",
            "audio.position.jump",
            "audio.position.shake",
            "audio.rotation.wobble",
            "audio.opacity.flash",
            "audio.envelope.attack_release"
        ];

        for (let recId of audioRecipes) {
            const recipe = global.vac34_RecipeRegistry.getRecipeById(recId);
            const expr = recipe.generateExpression(
                mockLayer,
                false,
                "vac34_Master_Controls",
                {},
                complexAudioName,
                complexChannelName
            );

            // Validate that generated expression parses cleanly as valid JS function
            try {
                new Function('thisComp', 'time', 'value', 'ease', expr);
            } catch (syntaxErr) {
                console.error("P1 VIOLATION: Audio escaping generated invalid JS in " + recId + ":\\n" + syntaxErr.message + "\\nExpression:\\n" + expr);
                process.exit(1);
            }
        }

        console.log("PASS: All 6 audio recipe generators handle complex quoted strings safely.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P1 audio escaping test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p1_project_save_reopen_rig_preservation(self):
        """P1 Regression: Project save/reopen preserves generated rigs via comment metadata."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
        new Function('thisObj', bundle)(global);

        const recipe = global.vac34_RecipeRegistry.getRecipeById("physics.spring.inertia");
        const existingEffects = [
            {
                name: "vac34 — Inertial Keyframe Bounce — Bounce Freq",
                matchName: "ADBE Slider Control",
                property: () => ({ value: 5.5, setValue: () => {} })
            },
            {
                name: "vac34 — Inertial Keyframe Bounce — Decay Damping",
                matchName: "ADBE Slider Control",
                property: () => ({ value: 7.0, setValue: () => {} })
            }
        ];

        const effectsGroup = {
            property: (n) => {
                for (let e of existingEffects) {
                    if (e.name === n) return e;
                }
                return null;
            }
        };

        // Layer restored from saved project with rig metadata in comment
        const reopenedLayer = {
            name: "ReopenedLayer",
            comment: "User custom comment\\n/* [vac34_rig:physics.spring.inertia] */",
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroup : null
        };

        for (let eff of existingEffects) {
            const isOwned = global.vac34_ControllerManager.isOwnedControl(reopenedLayer, recipe, eff);
            if (!isOwned) {
                console.error("P1 VIOLATION: Reopened layer rig control not recognized as owned: " + eff.name);
                process.exit(1);
            }
        }

        console.log("PASS: Saved/reopened rig controls recognized as owned.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P1 save/reopen test failed:\n{proc.stderr}\n{proc.stdout}")

    def test_p0_dockable_panel_startup_and_blank_panel_prevention(self):
        """P0 Regression: Dockable panel startup, root layout execution, and blank panel prevention."""
        node_script = """
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        function MockElement(type, text, val) {
            this.type = type;
            this.text = (typeof text === "string") ? text : "";
            this.selection = null;
            this.items = [];
            this.children = [];
            this.enabled = true;
            this.value = (typeof val === "number") ? val : 0;
            this.layoutCalls = 0;
            this.resizeCalls = 0;
            this.layout = {
                layout: () => { this.layoutCalls++; },
                resize: () => { this.resizeCalls++; }
            };
        }
        MockElement.prototype.add = function(t, bounds, a1, a2, a3) {
            if (t === "item") {
                const item = { text: a1 || "", index: this.items.length };
                this.items.push(item);
                return item;
            }
            const elem = new MockElement(t, (typeof a1 === "string" ? a1 : ""), (typeof a1 === "number" ? a1 : 0));
            elem.parent = this;
            this.children.push(elem);
            return elem;
        };
        MockElement.prototype.removeAll = function() { this.items = []; };
        MockElement.prototype.remove = function(child) {
            const idx = this.children.indexOf(child);
            if (idx !== -1) this.children.splice(idx, 1);
        };

        function MockPanel() {
            MockElement.call(this, "panel", "");
        }
        MockPanel.prototype = Object.create(MockElement.prototype);
        MockPanel.prototype.constructor = MockPanel;

        global.Panel = MockPanel;

        let windowInstances = [];
        function MockWindow(type, title) {
            MockElement.call(this, type, title);
            this.centered = false;
            this.shown = false;
            this.center = () => { this.centered = true; };
            this.show = () => { this.shown = true; };
            windowInstances.push(this);
        }
        MockWindow.prototype = Object.create(MockElement.prototype);
        MockWindow.prototype.constructor = MockWindow;
        global.Window = MockWindow;

        global.ScriptUI = {
            newFont: () => ({})
        };

        global.app = {
            project: { activeItem: null }
        };

        // 1. Test startup as docked Panel
        const mockDockedPanel = new MockPanel();

        // Run bundle passing mockDockedPanel as thisObj and this context
        new Function('thisObj', bundle).call(mockDockedPanel, mockDockedPanel);

        // Check 1: Root panel layout calls
        if (mockDockedPanel.layoutCalls < 1) {
            console.error("FAIL: Root docked panel layout() was NOT called!");
            process.exit(1);
        }
        if (mockDockedPanel.resizeCalls < 1) {
            console.error("FAIL: Root docked panel resize() was NOT called!");
            process.exit(2);
        }

        // Check 2: No Window instance should be spawned when running docked
        if (windowInstances.length !== 0) {
            console.error("FAIL: Window instance was created during docked Panel startup: " + windowInstances.length);
            process.exit(3);
        }

        // Check 3: Child controls exist
        if (mockDockedPanel.children.length === 0) {
            console.error("FAIL: Docked panel has no child controls!");
            process.exit(4);
        }

        // Check 4: Selected recipe exists
        const selRecipe = mockDockedPanel.getCurrentSelectedRecipe();
        if (!selRecipe) {
            console.error("FAIL: Initial recipe was not selected!");
            process.exit(5);
        }

        // Check 5: Parameters rendered
        const ctrlMap = mockDockedPanel.getParamControlMap();
        if (!ctrlMap || Object.keys(ctrlMap).length === 0) {
            console.error("FAIL: Recipe parameter controls were not rendered!");
            process.exit(6);
        }

        // Check 6: Startup stage is Panel ready
        if (global.vac34_Diagnostics.getCurrentStartupStage() !== "7. Panel ready") {
            console.error("FAIL: Startup stage is not '7. Panel ready': " + global.vac34_Diagnostics.getCurrentStartupStage());
            process.exit(7);
        }

        // Check 7: Test startup exception handling
        const faultyPanel = new MockPanel();
        faultyPanel.add = function(type, bounds, a1, a2, a3) {
            if (type === "group" && this.children.length === 2) {
                throw new Error("Simulated ScriptUI Control Creation Crash");
            }
            return MockElement.prototype.add.call(this, type, bounds, a1, a2, a3);
        };

        let caught = false;
        let alertMsg = null;
        global.alert = function(msg) { alertMsg = msg; };

        try {
            global.vac34_UIBuilder.build(faultyPanel);
        } catch (e) {
            caught = true;
        }

        if (!caught) {
            console.error("FAIL: Faulty build did not throw exception!");
            process.exit(8);
        }

        const startupErr = global.vac34_Diagnostics.getStartupError();
        if (!startupErr || startupErr.stage !== "4. Controls created") {
            console.error("FAIL: Diagnostics did not capture failed stage '4. Controls created': " + JSON.stringify(startupErr));
            process.exit(9);
        }

        // Verify faulty panel has error UI and is NOT completely blank
        if (faultyPanel.children.length === 0) {
            console.error("FAIL: Faulty panel left completely blank!");
            process.exit(10);
        }

        const errUiPanel = faultyPanel.children[0];
        if (!errUiPanel.text || errUiPanel.text.indexOf("Initialization Failure") === -1) {
            console.error("FAIL: Error UI panel header missing or incorrect: " + errUiPanel.text);
            process.exit(11);
        }

        // Check 8: Test floating Window mode (when thisObj is not a Panel)
        windowInstances = [];
        const floatingWin = global.vac34_UIBuilder.build(null);
        if (windowInstances.length !== 1) {
            console.error("FAIL: Floating Window not created when thisObj is null");
            process.exit(12);
        }
        if (!(floatingWin instanceof MockWindow)) {
            console.error("FAIL: Floating UI is not a Window instance");
            process.exit(13);
        }

        console.log("PASS: Docked panel startup, blank panel prevention, and diagnostics verified.");
        process.exit(0);
        """
        proc = subprocess.run(["node", "-e", node_script], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"P0 blank panel prevention test failed:\n{proc.stderr}\n{proc.stdout}")

if __name__ == "__main__":
    unittest.main()
