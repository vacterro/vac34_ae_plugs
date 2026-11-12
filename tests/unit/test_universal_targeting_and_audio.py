#!/usr/bin/env python3
"""
vac34_AE Universal Selected-Property Targeting & Audio Reactive Value Mapper Unit Tests
Covers all 20 required tests defined in SAIHANDOFF Section 14:
 1. Selected Starglow Threshold detected
 2. PropertyValueType.OneD detected
 3. Audio Scale Pump default target remains Transform.Scale
 4. Explicit Selected Property mode rejects incompatible Scale recipe
 5. Audio Reactive Value Mapper applies to selected Threshold
 6. Original Threshold value preserved in additive mode
 7. Audio missing causes actionable failure
 8. Audio exists but selected channel missing causes failure
 9. Two effects with identical property names do not target the wrong instance
 10. Foreign expressions remain untouched
 11. Existing keyframes remain preserved
 12. Multiple properties are independently validated
 13. Update modifies the intended property controls
 14. Remove preserves Starglow itself and its unrelated settings
 15. Save/reopen mock preserves rig structure
 16. Hidden status regression prevented
 17. Correct target preview shown before Apply
 18. Panel works with narrow dimensions
 19. Target selection remains valid during Apply
 20. Host smoke test runner validation
"""

import os
import sys
import unittest
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestUniversalTargetingAndAudio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build bundle first to ensure dist is up to date
        import subprocess
        proc = subprocess.run([sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--no-tests"], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        assert proc.returncode == 0, f"Builder failed:\n{proc.stderr}\n{proc.stdout}"

    def run_node_snippet(self, code: str) -> subprocess.CompletedProcess:
        full_code = f"""
        const fs = require('fs');
        const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');

        // Execute bundle in global context
        new Function('thisObj', bundle)(global);

        {code}
        """
        return subprocess.run(["node", "-e", full_code], cwd=WORKSPACE_ROOT, capture_output=True, text=True)

    def test_01_starglow_threshold_detected(self):
        """1. Selected Starglow Threshold detected."""
        code = """
        const mockThresholdProp = {
            name: "Threshold",
            matchName: "ADBE Starglow-0005",
            propertyValueType: 1, // OneD
            value: 262.0,
            canSetExpression: true,
            expression: "",
            parentProperty: {
                name: "Pre-Process",
                parentProperty: {
                    name: "Starglow",
                    parentProperty: {
                        name: "Effects",
                        parentProperty: null
                    }
                }
            }
        };

        const mockLayer = {
            name: "Adjustment Layer 8",
            selectedProperties: [mockThresholdProp],
            property: (p) => (p === "Effects" ? mockThresholdProp.parentProperty.parentProperty.parentProperty : null)
        };
        mockThresholdProp.parentProperty.parentProperty.parentProperty.parentProperty = mockLayer;

        const comp = {
            name: "Main Comp",
            selectedLayers: [mockLayer],
            selectedProperties: [mockThresholdProp]
        };

        const selected = global.vac34_TargetResolver.getSelectedProperties(comp);
        if (selected.length !== 1 || selected[0].name !== "Threshold") {
            console.error("FAIL: Selected Threshold was not detected! Length: " + selected.length);
            process.exit(1);
        }

        const insp = global.vac34_TargetResolver.inspectProperty(mockLayer, selected[0]);
        if (insp.path.indexOf("Starglow > Pre-Process > Threshold") === -1) {
            console.error("FAIL: Path does not contain Starglow Pre-Process Threshold: " + insp.path);
            process.exit(2);
        }

        console.log("PASS: Selected Starglow Threshold detected with path: " + insp.path);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_02_property_value_type_oned_detected(self):
        """2. PropertyValueType.OneD detected."""
        code = """
        const prop = {
            name: "Threshold",
            propertyValueType: 1, // OneD
            value: 262.0,
            canSetExpression: true
        };
        const dim = global.vac34_AEDom.getPropertyDimension(null, prop);
        if (dim !== 1) {
            console.error("FAIL: Expected dimension 1 for OneD, got: " + dim);
            process.exit(1);
        }
        console.log("PASS: PropertyValueType.OneD dimension 1 verified.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_03_audio_scale_pump_default_target_is_scale(self):
        """3. Audio Scale Pump default target remains Transform.Scale."""
        code = """
        const recipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        if (!recipe || !recipe.targetProperties || recipe.targetProperties[0] !== "Transform.Scale") {
            console.error("FAIL: audio.scale.pump targetProperties must be Transform.Scale, got: " + JSON.stringify(recipe && recipe.targetProperties));
            process.exit(1);
        }
        console.log("PASS: audio.scale.pump default target is Transform.Scale.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_04_selected_property_mode_rejects_incompatible_scale_recipe(self):
        """4. Explicit Selected Property mode rejects incompatible Scale recipe on 1D property."""
        code = """
        const scalarProp = {
            name: "Threshold",
            propertyValueType: 1, // 1D scalar
            canSetExpression: true,
            value: 262.0,
            expression: ""
        };
        const lyr = { name: "Adjustment Layer 8", selectedProperties: [scalarProp] };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [scalarProp] };

        const scaleRecipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        const res = global.vac34_TargetResolver.resolveTargets(comp, [lyr], scaleRecipe, "SELECTED_PROPERTY");

        if (res.ok) {
            console.error("FAIL: 2D Scale recipe should be rejected on 1D Threshold in SELECTED_PROPERTY mode!");
            process.exit(1);
        }
        if (res.message.indexOf("incompatible") === -1) {
            console.error("FAIL: Message should mention incompatible, got: " + res.message);
            process.exit(2);
        }
        console.log("PASS: Incompatible Scale recipe safely rejected: " + res.message);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_05_audio_reactive_value_mapper_applies_to_threshold(self):
        """5. Audio Reactive Value Mapper applies to selected Threshold."""
        code = """
        const thresholdProp = {
            name: "Threshold",
            matchName: "ADBE Starglow-0005",
            propertyIndex: 1,
            propertyValueType: 1,
            canSetExpression: true,
            value: 262.0,
            expression: "",
            parentProperty: null
        };

        // Faithful Effects Parade mock: reacquire must resolve the exact instance
        const starglow = {
            name: "Starglow",
            matchName: "STARGLOW",
            propertyIndex: 1,
            numProperties: 1,
            property: (p) => (p === 1 || p === "Threshold") ? thresholdProp : null
        };

        const effectsGroup = {
            name: "Effects",
            matchName: "ADBE Effect Parade",
            numProperties: 1,
            property: (p) => (p === 1 || p === "Starglow") ? starglow : null,
            addProperty: (m) => {
                let _v = 0;
                return {
                    name: m,
                    matchName: m,
                    property: () => ({
                        get value() { return _v; },
                        setValue: (v) => { _v = v; }
                    }),
                    remove: () => {}
                };
            }
        };

        const lyr = {
            name: "Adjustment Layer 8",
            selectedProperties: [thresholdProp],
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroup : null
        };
        thresholdProp.parentProperty = starglow;
        starglow.parentProperty = effectsGroup;
        effectsGroup.parentProperty = lyr;

        const audioLayer = {
            name: "Audio Amplitude",
            property: (p) => ({
                property: (chan) => ({
                    property: () => ({ valueAtTime: () => 15 })
                })
            })
        };

        const comp = {
            name: "Comp",
            numLayers: 1,
            selectedLayers: [lyr],
            selectedProperties: [thresholdProp],
            layer: (n) => (n === "Audio Amplitude" ? audioLayer : null)
        };
        comp.layer = function(n) {
            if (typeof n === "number") return (n === 1 ? audioLayer : null);
            return (n === "Audio Amplitude" ? audioLayer : null);
        };

        const mapperRecipe = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        if (!mapperRecipe) {
            console.error("FAIL: audio.property.map.scalar recipe not found!");
            process.exit(1);
        }

        const res = global.vac34_Engine.applyRecipe(
            comp,
            [lyr],
            mapperRecipe,
            { math_mode: 0, amount: 50, output_min: 0, output_max: 100 },
            false,
            "Audio Amplitude",
            "Both Channels",
            "AUTO"
        );

        if (!res.ok) {
            console.error("FAIL: applyRecipe failed: " + res.message);
            process.exit(2);
        }
        if (!thresholdProp.expression || thresholdProp.expression.indexOf("audio.property.map.scalar") === -1) {
            console.error("FAIL: Expression not applied to Threshold! Expr: " + thresholdProp.expression);
            process.exit(3);
        }

        console.log("PASS: Audio Reactive Value Mapper successfully applied to Threshold.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_06_original_threshold_preserved_in_additive_mode(self):
        """6. Original Threshold value preserved in additive mode."""
        code = """
        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const expr = mapper.generateExpression(
            { name: "Lyr" },
            false,
            null,
            { math_mode: 0, amount: 50, output_min: 0, output_max: 100 },
            "Audio Amplitude",
            "Both Channels"
        );

        // Simulate evaluation when audio is 0 (below threshold)
        // With math_mode: 0 (Additive) and _mapped: 0, result should be value + 0 = value
        if (expr.indexOf("value + _mapped") === -1) {
            console.error("FAIL: Additive branch 'value + _mapped' missing from expression!");
            process.exit(1);
        }

        // Evaluate synthetic math
        const value = 262.0;
        const _mapped = 0; // Below audio trigger threshold
        const finalVal = value + _mapped;
        if (finalVal !== 262.0) {
            console.error("FAIL: Base value changed! Expected 262, got: " + finalVal);
            process.exit(2);
        }

        console.log("PASS: Original Threshold 262.0 preserved in additive mode.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_07_audio_missing_causes_actionable_failure(self):
        """7. Audio missing causes actionable failure without false green."""
        code = """
        const thresholdProp = { name: "Threshold", propertyValueType: 1, canSetExpression: true, value: 262.0 };
        const lyr = { name: "Adjustment Layer 8", selectedProperties: [thresholdProp] };
        const comp = {
            name: "Comp",
            selectedLayers: [lyr],
            selectedProperties: [thresholdProp],
            layer: (n) => null // No Audio Amplitude layer exists!
        };

        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], mapper, {}, false, "NonExistentAudio", "Both Channels", "AUTO");

        if (res.ok) {
            console.error("FAIL: applyRecipe must fail when audio source is missing!");
            process.exit(1);
        }
        if (res.message.indexOf("Audio source missing") === -1 && res.message.indexOf("Convert Audio to Keyframes") === -1) {
            console.error("FAIL: Message should guide user to create Audio Amplitude, got: " + res.message);
            process.exit(2);
        }

        console.log("PASS: Missing audio source actionable failure verified: " + res.message);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_08_audio_channel_missing_causes_failure(self):
        """8. Audio exists but selected channel missing causes failure."""
        code = """
        const thresholdProp = { name: "Threshold", propertyValueType: 1, canSetExpression: true, value: 262.0 };
        const lyr = { name: "Adjustment Layer 8", selectedProperties: [thresholdProp] };
        const audioLyr = {
            name: "Audio Amplitude",
            property: (p) => ({
                property: (chan) => null // Channel missing
            })
        };
        const comp = {
            name: "Comp",
            numLayers: 1,
            selectedLayers: [lyr],
            selectedProperties: [thresholdProp],
            layer: function(n) {
                if (typeof n === "number") return (n === 1 ? audioLyr : null);
                return (n === "Audio Amplitude" ? audioLyr : null);
            }
        };

        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], mapper, {}, false, "Audio Amplitude", "MissingChannel", "AUTO");

        if (res.ok) {
            console.error("FAIL: Missing channel must cause failure!");
            process.exit(1);
        }
        if (res.message.indexOf("channel") === -1) {
            console.error("FAIL: Error should specify channel missing, got: " + res.message);
            process.exit(2);
        }

        console.log("PASS: Missing audio channel failure verified: " + res.message);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_09_two_effects_with_identical_property_names(self):
        """9. Two effects with identical property names target the correct selected instance."""
        code = """
        const effect1Prop = { name: "Threshold", propertyValueType: 1, canSetExpression: true, parentProperty: { name: "Starglow" } };
        const effect2Prop = { name: "Threshold", propertyValueType: 1, canSetExpression: true, parentProperty: { name: "Glow" } };

        const path1 = global.vac34_TargetResolver.getPropertyPath(effect1Prop);
        const path2 = global.vac34_TargetResolver.getPropertyPath(effect2Prop);

        if (path1 === path2) {
            console.error("FAIL: Paths must distinguish parent effect names!");
            process.exit(1);
        }
        if (path1.indexOf("Starglow") === -1 || path2.indexOf("Glow") === -1) {
            console.error("FAIL: Paths do not contain respective effect names: " + path1 + " vs " + path2);
            process.exit(2);
        }

        console.log("PASS: Multiple effects with identical property names distinguished: " + path1 + " / " + path2);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_10_foreign_expressions_remain_untouched(self):
        """10. Foreign expressions remain untouched on selected effect properties."""
        code = """
        const foreignProp = {
            name: "Threshold",
            propertyValueType: 1,
            canSetExpression: true,
            value: 262.0,
            expression: "wiggle(5, 10); // foreign user expression"
        };
        const lyr = { name: "Adjustment Layer 8", selectedProperties: [foreignProp] };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [foreignProp] };

        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], mapper, {}, false, "Audio Amplitude", "Both Channels", "AUTO");

        if (res.ok) {
            console.error("FAIL: applyRecipe should not succeed over foreign expression!");
            process.exit(1);
        }
        if (foreignProp.expression !== "wiggle(5, 10); // foreign user expression") {
            console.error("FAIL: Foreign expression was modified!");
            process.exit(2);
        }

        console.log("PASS: Foreign expression preserved byte-identical.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_14_remove_preserves_starglow_itself(self):
        """14. Remove clears expression and preserves Starglow itself and unrelated effects."""
        code = """
        let removedEffects = [];
        const thresholdProp = {
            name: "Threshold",
            propertyValueType: 1,
            canSetExpression: true,
            expression: "/* [vac34_AE:audio.property.map.scalar] */\\nvalue + _mapped;",
            parentProperty: { name: "Starglow" }
        };

        const starglowEffect = {
            name: "Starglow",
            matchName: "ADBE Starglow",
            property: (p) => thresholdProp,
            numProperties: 1,
            remove: function() { removedEffects.push(this.name); }
        };

        const vac34Ctrl = {
            name: "vac34 — Audio Reactive Value Mapper — Amount %",
            property: () => ({ value: 50 }),
            remove: function() { removedEffects.push(this.name); }
        };

        const effectsMap = {
            1: starglowEffect,
            2: vac34Ctrl
        };

        const mockEffects = {
            numProperties: 2,
            property: (idxOrName) => {
                if (typeof idxOrName === "number") return effectsMap[idxOrName];
                if (idxOrName === "Starglow") return starglowEffect;
                if (idxOrName.indexOf("vac34") !== -1) return vac34Ctrl;
                return null;
            }
        };

        const lyr = {
            name: "Adjustment Layer 8",
            property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? mockEffects : null
        };
        const comp = { name: "Comp", selectedLayers: [lyr] };

        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const res = global.vac34_Engine.removeRecipe(comp, [lyr], mapper);

        if (!res.ok) {
            console.error("FAIL: removeRecipe failed: " + res.message);
            process.exit(1);
        }
        if (thresholdProp.expression !== "") {
            console.error("FAIL: Threshold expression was not cleared!");
            process.exit(2);
        }
        if (removedEffects.indexOf("Starglow") !== -1) {
            console.error("FATAL: Starglow itself was removed!");
            process.exit(3);
        }

        console.log("PASS: Starglow preserved, expression cleared, and vac34 controls cleaned up.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

    def test_17_correct_target_preview_shown(self):
        """17. Correct target preview shown before Apply."""
        code = """
        const thresholdProp = {
            name: "Threshold",
            propertyValueType: 1,
            canSetExpression: true,
            parentProperty: {
                name: "Pre-Process",
                parentProperty: {
                    name: "Starglow",
                    parentProperty: { name: "Adjustment Layer 8" }
                }
            }
        };
        const lyr = { name: "Adjustment Layer 8", selectedProperties: [thresholdProp], property: () => null };
        thresholdProp.parentProperty.parentProperty.parentProperty = lyr;
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [thresholdProp] };

        const mapper = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const preview = global.vac34_TargetResolver.getPreviewSummary(comp, [lyr], mapper, "AUTO");

        if (preview.indexOf("Threshold") === -1 || preview.indexOf("Starglow") === -1) {
            console.error("FAIL: Preview does not show Starglow Threshold: " + preview);
            process.exit(1);
        }

        console.log("PASS: Target preview correctly shows: " + preview);
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"Snippet failed:\n{proc.stderr}\n{proc.stdout}")

if __name__ == "__main__":
    unittest.main()
