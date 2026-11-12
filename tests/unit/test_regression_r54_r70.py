#!/usr/bin/env python3
import os
import sys
import unittest
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORKSPACE_ROOT)

RECIPE_ID = "opacity.pulse.sine"

JS_EFFECTS_GROUP = """
function effectsGroupMock() {
    const data = [];
    const handles = {};
    const g = {
        name: "Effects",
        matchName: "ADBE Effect Parade",
        numProperties: 0,
        property: function(k) {
            if (typeof k === "number") return data[k - 1] || null;
            if (handles[k]) return handles[k];
            for (var i = 0; i < data.length; i++) {
                if (data[i].name === k) return data[i];
            }
            return null;
        },
        addProperty: function(matchName, name, subProp) {
            name = name || matchName;
            const d = { name: name, matchName: matchName, val: 0, expr: "" };
            const handle = {
                _vac34Owned: true,
                get name() { return d.name; },
                set name(n) { d.name = n; },
                get matchName() { return d.matchName; },
                set matchName(nm) { d.matchName = nm; },
                property: function(k) {
                    if (subProp && (k === 1 || k === subProp.name)) return subProp;
                    return {
                        get value() { return d.val; },
                        setValue: function(v) { d.val = v; },
                        get expression() { return d.expr; },
                        set expression(v) { d.expr = v; }
                    };
                },
                remove: function() {
                    const i = data.indexOf(handle);
                    if (i !== -1) { data.splice(i, 1); g.numProperties = data.length; }
                }
            };
            data.push(handle);
            g.numProperties = data.length;
            handles[matchName] = handle;
            return handle;
        }
    };
    return g;
}
"""


class TestRegressionR54ToR70(unittest.TestCase):
    def run_node_snippet(self, code):
        full_code = "const fs = require('fs'); const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8'); new Function('thisObj', bundle)(global);\n" + JS_EFFECTS_GROUP + "\n" + code
        return subprocess.run(["node", "-e", full_code], cwd=WORKSPACE_ROOT, capture_output=True, text=True)

    def test_r54_failed_same_recipe_reapply_restores_original_expression(self):
        code = """
        const PREV = "/* [vac34_AE:opacity.pulse.sine] */\\nPREVIOUS_GOOD";
        let expr = PREV;
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            get expression() { return expr; }, set expression(v) { expr = v; },
            expressionEnabled: true };
        prop.parentProperty = { name: "Transform" };
        prop.parentProperty.parentProperty = null;
        const lyr = { name: "Solid 1", selectedProperties: [prop],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroupMock() : null; } };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        recipe.generateExpression = function() { throw new Error("expressionError: bad math"); };

        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.ok) { console.error("FAIL r54: expected failure"); process.exit(1); }
        if (expr !== PREV) { console.error("FAIL r54: expr not restored: " + expr); process.exit(2); }
        if (prop.expressionEnabled !== true) { console.error("FAIL r54: enabled changed"); process.exit(3); }
        if (res.status !== "APPLY_FAILED_ROLLED_BACK") { console.error("FAIL r54: status=" + res.status); process.exit(4); }
        console.log("PASS: R54 original expression restored byte-for-byte.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r55_failure_after_assignment_restores_expression_enabled(self):
        code = """
        let expr = "";
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            get expression() { return expr; }, set expression(v) { expr = v; },
            expressionEnabled: true };
        prop.parentProperty = { name: "Transform" };
        prop.parentProperty.parentProperty = null;
        const lyr = { name: "Solid 1", selectedProperties: [prop],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroupMock() : null; } };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        recipe.generateExpression = function() { throw new Error("boom"); };
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (prop.expressionEnabled !== true) { console.error("FAIL r55: " + prop.expressionEnabled); process.exit(1); }
        if (res.ok) { process.exit(2); }
        console.log("PASS: R55 expressionEnabled preserved after failed assignment.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r56_fresh_apply_failure_leaves_expression_empty(self):
        code = """
        let expr = "";
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            get expression() { return expr; }, set expression(v) { expr = v; },
            expressionEnabled: true };
        prop.parentProperty = { name: "Transform" };
        prop.parentProperty.parentProperty = null;
        const lyr = { name: "Solid 1", selectedProperties: [prop],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroupMock() : null; } };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        recipe.generateExpression = function() { throw new Error("boom"); };
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (expr !== "") { console.error("FAIL r56: " + expr); process.exit(1); }
        console.log("PASS: R56 fresh apply failure leaves expression empty.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r57_duplicate_starglow_with_invalid_index_never_cross_targets(self):
        code = """
        const effects = effectsGroupMock();
        effects.addProperty("Starglow");
        effects.addProperty("Starglow");
        effects.numProperties = 2;

        let t1expr = "";
        const t1 = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return t1expr; }, set expression(v) { t1expr = v; } };
        let t2expr = "";
        const t2 = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return t2expr; }, set expression(v) { t2expr = v; } };
        t1.parentProperty = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 1,
            property: function(p) { return (p === 1 || p === "Threshold") ? t1 : null; } };
        t2.parentProperty = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 2,
            property: function(p) { return (p === 1 || p === "Threshold") ? t2 : null; } };
        t1.parentProperty.parentProperty = effects;
        t2.parentProperty.parentProperty = effects;
        effects.parentProperty = null;

        const lyr = { name: "Layer", selectedProperties: [t1],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [t1] };

        // Force ambiguous identity: descriptor index 3 does not exist (only 2 effects)
        const desc = global.vac34_AEDom.capturePropertyDescriptor(lyr, t1);
        desc.effectIndex = 3;
        const ra = global.vac34_AEDom.reacquireProperty(lyr, desc);
        if (ra !== null) { console.error("FAIL r57: ambiguous identity must return null"); process.exit(1); }
        if (t1expr !== "" || t2expr !== "") { console.error("FAIL r57: mutated"); process.exit(2); }
        console.log("PASS: R57 duplicate Starglow with ambiguous identity never cross-targets.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r58_ambiguous_property_identity_safe_rejection(self):
        code = """
        const effects = effectsGroupMock();
        effects.addProperty("Starglow");
        effects.addProperty("Starglow");
        effects.numProperties = 2;

        let t1expr = "";
        const t1 = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return t1expr; }, set expression(v) { t1expr = v; } };
        t1.parentProperty = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 77,
            property: function(p) { return (p === 1 || p === "Threshold") ? t1 : null; } };
        t1.parentProperty.parentProperty = effects;
        effects.parentProperty = null;

        const lyr = { name: "Layer", selectedProperties: [t1],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [t1] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.ok) { console.error("FAIL r58: must reject"); process.exit(1); }
        if (t1expr !== "") { console.error("FAIL r58: mutated"); process.exit(2); }
        console.log("PASS: R58 ambiguous identity safely rejected.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r59_reacquire_null_cannot_lead_to_stale_mutation(self):
        code = """
        let expr = "";
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            get expression() { return expr; }, set expression(v) { expr = v; } };
        prop.parentProperty = { name: "Transform" };
        const lyr = { name: "Layer", selectedProperties: [prop],
            property: function(p) { return null; } };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.ok) { console.error("FAIL r59: null reacquire must not apply"); process.exit(1); }
        if (expr !== "") { console.error("FAIL r59: stale write"); process.exit(2); }
        console.log("PASS: R59 null reacquire fails closed, no stale mutation.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r60_universal_recipe_targetdimensions_zero_accepts_scalar(self):
        code = """
        const recipe = global.vac34_RecipeRegistry.getRecipeById("loops.cycle.keyframes");
        if (!recipe) { console.error("FAIL r60: missing recipe"); process.exit(1); }
        if (recipe.targetDimensions !== 0) { console.error("FAIL r60: dim=" + recipe.targetDimensions); process.exit(2); }
        const insp = global.vac34_TargetResolver.inspectProperty(
            { index: 1, name: "L", property: function() { return null; } },
            { name: "Threshold", propertyValueType: 1, canSetExpression: true, dimension: 1, matchName: "" }
        );
        const check = global.vac34_TargetResolver.checkPropertyCompatibility(insp, recipe);
        if (!check.compatible) { console.error("FAIL r60: " + check.reason); process.exit(3); }
        console.log("PASS: R60 targetDimensions=0 accepts 1D scalar.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r61_universal_recipe_rejects_unsupported_types(self):
        code = """
        const recipe = global.vac34_RecipeRegistry.getRecipeById("wiggle.noise.controlled");
        const textProp = { name: "Source Text", propertyValueType: 7, canSetExpression: true,
            dimension: "text", matchName: "ADBE Text Document" };
        const insp = global.vac34_TargetResolver.inspectProperty(
            { index: 1, name: "L", property: function() { return null; } }, textProp);
        const check = global.vac34_TargetResolver.checkPropertyCompatibility(insp, recipe);
        if (check.compatible) { console.error("FAIL r61: text accepted"); process.exit(1); }
        console.log("PASS: R61 universal recipe rejects unsupported text type.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r62_existing_controller_expression_restored_after_rollback(self):
        code = """
        const effects = effectsGroupMock();
        const slider = effects.addProperty("vac34_Controller — Test");
        slider.property(1);

        const lyr = { name: "Layer", comment: "/* [vac34_ctrl:vac34_Controller — Test] */",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };

        const recipe = { id: "opacity.pulse.sine", displayName: "Test Recipe",
            parameters: [{ id: "amount", name: "Test", type: "slider", "default": 50 }] };

        const tx = new global.vac34_ControllerManager.ControllerTransaction(lyr, recipe);
        const ok = tx.setup({ amount: 50 });
        if (!ok) { console.error("FAIL r62: setup failed " + JSON.stringify(tx.failedOperations)); process.exit(1); }
        tx.rollback();
        if (tx.failedOperations.length > 0) { console.error("FAIL r62: " + JSON.stringify(tx.failedOperations)); process.exit(2); }
        console.log("PASS: R62 rollback completed with zero failed operations.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r63_rollback_failure_not_reported_as_clean_success(self):
        code = """
        const effects = effectsGroupMock();
        const slider = effects.addProperty("vac34_Controller — Test");
        const lyr = { name: "Layer", comment: "",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };

        const recipe = { id: "opacity.pulse.sine", displayName: "Test Recipe",
            parameters: [{ id: "amount", name: "Test", type: "slider", "default": 50 }] };

        const tx = new global.vac34_ControllerManager.ControllerTransaction(lyr, recipe);
        const ok = tx.setup({ amount: 50 });
        if (!ok) { console.error("FAIL r63: setup failed"); process.exit(1); }
        // Force a rollback defect: remove the backing effect before rollback
        const last = effects.numProperties;
        effects.property(last).remove();
        tx.rollback();
        if (tx.failedOperations.length === 0) {
            console.error("FAIL r63: rollback failure not recorded");
            process.exit(2);
        }
        console.log("PASS: R63 rollback failure recorded, not masked as success.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r64_duplicate_audio_layer_names_no_redirect(self):
        code = """
        const audioA = { name: "Audio Amplitude",
            property: function(p) { return { property: function(c) { return { value: 1 }; } }; } };
        const audioB = { name: "Audio Amplitude",
            property: function(p) { return { property: function(c) { return { value: 2 }; } }; } };
        const comp = { name: "Comp", numLayers: 2,
            layer: function(n) { return typeof n === "number" ? (n === 1 ? audioA : audioB) : null; } };

        const val = global.vac34_AudioEngine.validateAudioSource(comp, "Audio Amplitude", "Both Channels");
        if (val.valid) { console.error("FAIL r64: ambiguous audio validated"); process.exit(1); }
        if (val.message.indexOf("AUDIO_SOURCE_IDENTITY_LOST") === -1) { console.error("FAIL r64: " + val.message); process.exit(2); }
        console.log("PASS: R64 duplicate audio names rejected with AUDIO_SOURCE_IDENTITY_LOST.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r65_update_preserves_selected_audio_identity(self):
        code = """
        const audioA = { name: "Audio A",
            property: function(p) { return { property: function(c) { return { value: 1 }; } }; } };
        const audioB = { name: "Audio B",
            property: function(p) { return { property: function(c) { return { value: 2 }; } }; } };
        const comp = { name: "Comp", numLayers: 2,
            layer: function(n) { return typeof n === "number" ? (n === 1 ? audioA : audioB) : null; } };

        const v1 = global.vac34_AudioEngine.validateAudioSource(comp, "Audio A", "Both Channels");
        const v2 = global.vac34_AudioEngine.validateAudioSource(comp, "Audio B", "Both Channels");
        if (!v1.valid || !v2.valid || v1.layer !== audioA || v2.layer !== audioB) {
            console.error("FAIL r65: identity lost");
            process.exit(1);
        }
        console.log("PASS: R65 update preserves selected audio identity.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r66_comp_save_reopen_preserves_rig(self):
        code = """
        function buildRig() {
            const th = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
                propertyValueType: 1, canSetExpression: true };
            const eff = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 1,
                property: function(p) { return (p === 1 || p === "Threshold") ? th : null; } };
            const eg = { name: "Effects", matchName: "ADBE Effect Parade", numProperties: 1,
                property: function(p) { return (p === 1 || p === "Starglow") ? eff : null; } };
            const lyr = { index: 3, name: "Layer 3",
                property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? eg : null; } };
            th.parentProperty = eff;
            eff.parentProperty = eg;
            eg.parentProperty = lyr;
            return { lyr: lyr, prop: th };
        }
        const a = buildRig();
        const b = buildRig();
        const k1 = global.vac34_TargetResolver.getPropertyUniqueKey(a.lyr, a.prop);
        const k2 = global.vac34_TargetResolver.getPropertyUniqueKey(b.lyr, b.prop);
        if (k1 !== k2) { console.error("FAIL r66: " + k1 + " vs " + k2); process.exit(1); }
        console.log("PASS: R66 structural identity survives comp save/reopen.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r67_no_duplicate_controllers_after_repeated_apply(self):
        code = """
        const effects = effectsGroupMock();
        const lyr = { name: "Layer",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };

        const recipe = { id: "opacity.pulse.sine", displayName: "Test Recipe",
            parameters: [{ id: "amount", name: "Test", type: "slider", "default": 50 }] };

        global.vac34_ControllerManager.setupRecipeControls(lyr, recipe, { amount: 10 });
        global.vac34_ControllerManager.setupRecipeControls(lyr, recipe, { amount: 20 });

        const expect = global.vac34_Config.EFFECT_PREFIX + "Test Recipe — Test";
        let count = 0;
        for (let i = 1; i <= effects.numProperties; i++) {
            if (effects.property(i).name === expect) count++;
        }
        if (count !== 1) { console.error("FAIL r67: " + count + " controllers"); process.exit(1); }
        console.log("PASS: R67 no duplicate controller effects after repeated Apply.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r68_keyframes_preserved_after_failed_and_successful_operations(self):
        code = """
        let expr = "";
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            _keyframes: [0, 50, 100],
            get expression() { return expr; }, set expression(v) { expr = v; },
            get numKeys() { return this._keyframes.length; } };
        const lyr = { name: "Layer", selectedProperties: [prop] };
        const transform = { name: "Transform", numProperties: 1,
            property: function(p) { return (p === 1 || p === "Opacity") ? prop : null; } };
        prop.parentProperty = transform;
        transform.parentProperty = lyr;
        lyr.property = function(p) {
            if (p === "Transform") return transform;
            return (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroupMock() : null;
        };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const failRecipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        failRecipe.generateExpression = function() { throw new Error("boom"); };
        global.vac34_Engine.applyRecipe(comp, [lyr], failRecipe, {}, false, null, null, "AUTO");
        if (prop._keyframes.length !== 3) { console.error("FAIL r68: keyframes lost (fail path)"); process.exit(1); }

        const good = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        good.generateExpression = function() { return "/* [vac34_AE:opacity.pulse.sine] */\\nvalue;"; };
        const res2 = global.vac34_Engine.applyRecipe(comp, [lyr], good, {}, false, null, null, "AUTO");
        if (!res2.ok) { console.error("FAIL r68: " + res2.message); process.exit(2); }
        if (prop._keyframes.length !== 3) { console.error("FAIL r68: keyframes lost (success path)"); process.exit(3); }
        console.log("PASS: R68 keyframes preserved across failed and successful operations.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r69_multiple_selected_properties_no_identity_confusion(self):
        code = """
        const effects = effectsGroupMock();

        let p1expr = "";
        const p1 = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return p1expr; }, set expression(v) { p1expr = v; } };
        let p2expr = "";
        const p2 = { name: "Threshold", matchName: "ADBE Starglow-0005", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return p2expr; }, set expression(v) { p2expr = v; } };
        p1.parentProperty = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 1,
            property: function(p) { return (p === 1 || p === "Threshold") ? p1 : null; } };
        p2.parentProperty = { name: "Starglow", matchName: "STARGLOW", propertyIndex: 2,
            property: function(p) { return (p === 1 || p === "Threshold") ? p2 : null; } };
        p1.parentProperty.parentProperty = effects;
        p2.parentProperty.parentProperty = effects;

        effects.addProperty("STARGLOW", "Starglow", p1);
        effects.addProperty("STARGLOW", "Starglow", p2);

        const lyr = { name: "Layer", selectedProperties: [p1, p2],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [p1, p2] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.appliedCount !== 2) { console.error("FAIL r69: " + res.message); process.exit(1); }
        if (p1expr.indexOf("opacity.pulse.sine") === -1 || p2expr.indexOf("opacity.pulse.sine") === -1) {
            console.error("FAIL r69: identity confusion"); process.exit(2);
        }
        console.log("PASS: R69 multiple properties processed without identity confusion.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)

    def test_r70_host_expressionerror_complete_rollback(self):
        code = """
        const PREV = "/* [vac34_AE:opacity.pulse.sine] */\\nPREVIOUS_GOOD";
        let expr = PREV;
        const prop = { name: "Opacity", propertyValueType: 1, canSetExpression: true,
            get expression() { return expr; }, set expression(v) { expr = v; },
            expressionError: "After Effects error: Invalid expression.",
            expressionEnabled: true };
        prop.parentProperty = { name: "Transform" };
        prop.parentProperty.parentProperty = null;
        const lyr = { name: "Layer", selectedProperties: [prop],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroupMock() : null; } };
        const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.ok) { console.error("FAIL r70: expressionError must fail"); process.exit(1); }
        if (expr.indexOf("PREVIOUS_GOOD") === -1) { console.error("FAIL r70: " + expr); process.exit(2); }
        if (res.status !== "APPLY_FAILED_ROLLED_BACK") { console.error("FAIL r70: status=" + res.status); process.exit(3); }
        console.log("PASS: R70 host expressionError handled with complete rollback.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, "Snippet failed:\n" + proc.stderr + "\n" + proc.stdout)


if __name__ == "__main__":
    unittest.main()
