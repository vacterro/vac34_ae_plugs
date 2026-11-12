#!/usr/bin/env python3
"""
vac34_AE T-7 Regression Suite (R83-R105)
SAIHANDOFF T-7 (Sections 4-6, 13, 14) acceptance coverage:

  WAVE A PINNED compatibility:
    R83 PINNED rejects a 2D recipe on a 1D Threshold (no false SUCCESS).
    R84 PINNED does not bypass canSetExpression.
    R85 PINNED applies the correct scalar recipe.
    R86 PINNED rejects an unsupported PropertyValueType.
    R103 No false SUCCESS for an unsupported pinned recipe (postconditions).
  WAVE B controller ownership:
    R87 PINNED + Shared Master Update changes master controls only.
    R88 PINNED + Per-Layer Update changes target-layer controls only.
    R89 Update cannot report success when the wrong owner is modified.
  WAVE C remove lifecycle:
    R90 PINNED Remove cleans unreferenced owned controls.
    R91 PINNED Remove preserves shared controls with other consumers.
    R92 Remove never deletes unrelated effects.
    R93 Repeated Apply/Remove does not accumulate orphan controls.
  WAVE D UI geometry:
    R94 Narrow panel retains working action buttons (mock geometry).
    R95 Real ScrollUI viewport clip/scroll in actual AE — NOT_RUN (host).
    R96 Changing recipes recomputes scroll geometry.
  WAVE E audio identity:
    R97 Audio source identity survives Refresh (index-aware restore).
    R98 Duplicate audio names do not silently relink.
  WAVE F context stability:
    R99 Composition focus change does not retarget pinned property.
  WAVE G test infrastructure:
    R100 Portable tests never require personal Windows drives.
    R101 Clean archive rebuild is independent of live deployment.
    R102 Real Windows deployment checks actual hashes — gated.
  WAVE H real AE Glow acceptance:
    R104/R105 — NOT_RUN (need real After Effects 2024 host).
"""

import glob
import os
import subprocess
import sys
import unittest

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORKSPACE_ROOT)

from tests.unit.test_regression_r71_r82 import JS_EFFECTS_GROUP, JS_SCRIPTUI_MOCK

# Shared AE mock: pinned Glow Threshold fixture with real layer indexing
# (adding a master null shifts layer indexes, as in After Effects).
JS_PINNED_FIXTURE = """
function mkPinnedComp(opts) {
    opts = opts || {};
    let thrExpr = "";
    const thr = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
        propertyValueType: 1, canSetExpression: true, value: 60,
        expressionEnabled: true, expressionError: "",
        get expression() { return thrExpr; }, set expression(v) { thrExpr = v; } };
    if (opts.canSetExpression !== undefined) thr.canSetExpression = opts.canSetExpression;
    if (opts.valueType !== undefined) thr.propertyValueType = opts.valueType;

    const effects = effectsGroupMock();
    const glowHandle = effects.addProperty("ADBE Glow", "Glow", thr);
    glowHandle.property = function(k) { return (k === 1 || k === "Threshold") ? thr : null; };
    thr.parentProperty = glowHandle;
    glowHandle.parentProperty = effects;

    const layers = [];
    const lyr = { name: opts.layerName || "Glow Layer", index: 1, comment: "", selectedProperties: [],
        property(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
    effects.parentProperty = lyr;
    layers.push(lyr);

    if (opts.withAudio !== false) {
        const afx = effectsGroupMock();
        afx.addProperty("ADBE Slider Control", "Both Channels", { name: "Slider" });
        const alyr = { name: "Audio Amplitude", comment: "", selectedProperties: [],
            property(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? afx : null; } };
        afx.parentProperty = alyr;
        layers.push(alyr);
    }
    (opts.extraLayers || []).forEach(function(l) { layers.push(l); });

    function reindex() { layers.forEach(function(l, i) { l.index = i + 1; }); }

    const comp = {
        name: opts.name || "TestComp",
        get numLayers() { return layers.length; },
        selectedLayers: [], selectedProperties: [],
        layer: function(k) {
            if (typeof k === "number") return layers[k - 1] || null;
            if (typeof k === "string") { for (var i = 0; i < layers.length; i++) { if (layers[i].name === k) return layers[i]; } }
            return null;
        },
        layers: {
            addNull: function() {
                const nfx = effectsGroupMock();
                const nlyr = { name: "vac34_Master_Controls", comment: "", label: 0, guideLayer: false,
                    _vac34IsNew: true,
                    moveToBeginning: function() { layers.unshift(nlyr); reindex(); },
                    property(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? nfx : null; } };
                nfx.parentProperty = nlyr;
                layers.unshift(nlyr); reindex();
                return nlyr;
            }
        }
    };
    global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };
    return { comp: comp, layers: layers, lyr: lyr, thr: thr, effects: effects };
}

function masterEffects(fx) {
    return (fx.comp, fx.layers[0]);
}
"""

AUDIO_RECIPE_ID = "audio.property.map.scalar"


def audio_recipe_getter(extra=""):
    return ('global.vac34_RecipeRegistry.getRecipeById("%s")' % AUDIO_RECIPE_ID) + extra


class TestRegressionR83ToR105(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            [sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--no-tests"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        assert proc.returncode == 0, f"Builder failed:\n{proc.stderr}\n{proc.stdout}"

    def run_node_snippet(self, code):
        full_code = (
            "const fs = require('fs');\n"
            "const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');\n"
            "new Function('thisObj', bundle)(global);\n"
            + JS_EFFECTS_GROUP + "\n"
            + JS_SCRIPTUI_MOCK + "\n"
            + JS_PINNED_FIXTURE + "\n"
            + code
        )
        return subprocess.run(["node", "-e", full_code], cwd=WORKSPACE_ROOT, capture_output=True, text=True)

    # ------------------------------------------------------------------
    # WAVE A — PINNED compatibility gate
    # ------------------------------------------------------------------
    def test_r83_pinned_rejects_2d_recipe_on_1d_threshold(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const scaleRecipe = global.vac34_RecipeRegistry.getRecipeById("audio.scale.pump");
        if (!scaleRecipe || scaleRecipe.targetDimensions !== 2) { console.error("FAIL r83 setup"); process.exit(9); }
        const before = f.effects.numProperties;
        const res = global.vac34_Engine.applyRecipe(f.comp, [], scaleRecipe, {}, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (res.ok || res.status !== "TARGET_INCOMPATIBLE") { console.error("FAIL r83: " + JSON.stringify(res)); process.exit(1); }
        if (res.skipCount !== 1) { console.error("FAIL r83 skipCount: " + res.skipCount); process.exit(2); }
        if (f.effects.numProperties !== before) { console.error("FAIL r83: controller effects were created"); process.exit(3); }
        if (f.thr.expression !== "") { console.error("FAIL r83: expression was written"); process.exit(4); }
        console.log("PASS: R83 2D recipe on pinned 1D Threshold rejected.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R83 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r84_pinned_does_not_bypass_cansetexpression(self):
        code = """
        const f = mkPinnedComp({ canSetExpression: false });
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const before = f.effects.numProperties;
        const res = global.vac34_Engine.applyRecipe(f.comp, [], recipe, {}, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (res.ok || res.status !== "TARGET_INCOMPATIBLE") { console.error("FAIL r84: " + JSON.stringify(res)); process.exit(1); }
        if (res.message.indexOf("canSetExpression") === -1) { console.error("FAIL r84 reason: " + res.message); process.exit(2); }
        if (f.effects.numProperties !== before) { console.error("FAIL r84: controllers created"); process.exit(3); }
        console.log("PASS: R84 PINNED respects canSetExpression.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R84 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r85_pinned_applies_correct_scalar_recipe(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const res = global.vac34_Engine.applyRecipe(f.comp, [], recipe,
            { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 },
            false, "Audio Amplitude", "Both Channels", "PINNED");
        if (!res.ok || res.status !== "APPLIED_VERIFIED" || res.appliedCount !== 1) {
            console.error("FAIL r85: " + JSON.stringify(res)); process.exit(1);
        }
        const expr = f.thr.expression;
        if (expr.indexOf("[vac34_AE:%s]") === -1) { console.error("FAIL r85 tag"); process.exit(2); }
        if (expr.indexOf("value +") === -1) { console.error("FAIL r85 scalar expression shape: " + expr); process.exit(3); }
        if (expr.indexOf("[" + expr.indexOf("value") + "]") !== -1) { process.exit(4); }
        console.log("PASS: R85 scalar audio recipe pinned on Threshold.");
        process.exit(0);
        """ % (audio_recipe_getter(), AUDIO_RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R85 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r86_pinned_rejects_unsupported_propertyvaluetype(self):
        code = """
        const f = mkPinnedComp({ valueType: 7 });
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const res = global.vac34_Engine.applyRecipe(f.comp, [], recipe, {}, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (res.ok || res.status !== "TARGET_INCOMPATIBLE") { console.error("FAIL r86: " + JSON.stringify(res)); process.exit(1); }
        console.log("PASS: R86 text-valued property rejected for pinned apply.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R86 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r103_no_false_success_for_unsupported_pinned_recipe(self):
        """R103: an unsupported pinned recipe never reports ok/APPLIED.
        Uses real 2D scale recipe on 1D Threshold (incompatible dimensions).
        """
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing");
        if (!recipe || recipe.targetDimensions !== 2) { console.error("FAIL r103 setup: need 2D recipe"); process.exit(9); }
        const res = global.vac34_Engine.applyRecipe(f.comp, [], recipe, {}, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (res.ok) { console.error("FAIL r103: ok reported"); process.exit(1); }
        if (res.status === "APPLIED_VERIFIED" || res.status === "PARTIAL_SUCCESS" || res.appliedCount > 0) {
            console.error("FAIL r103 status: " + res.status); process.exit(2);
        }
        if (f.thr.expression !== "" || f.effects.numProperties !== 1) {
            console.error("FAIL r103 postconditions"); process.exit(3);
        }
        console.log("PASS: R103 no false SUCCESS for unsupported pinned recipe.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R103 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE B — controller ownership
    # ------------------------------------------------------------------
    def test_r87_pinned_master_update_changes_master_controls_only(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, true, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap.ok) { console.error("FAIL r87 apply: " + JSON.stringify(ap)); process.exit(1); }
        const master = global.vac34_ControllerManager.findMasterLayer(f.comp);
        if (!master) { console.error("FAIL r87: no master created"); process.exit(2); }
        const ctrl = master.property("ADBE Effect Parade").property(global.vac34_ControllerManager.getEffectPrefixForRecipe(recipe) + " \\u2014 Amount %%");
        if (!ctrl) { console.error("FAIL r87: master control missing"); process.exit(3); }
        const before = ctrl.property(1).value;
        const up = global.vac34_Engine.updateParameters(f.comp, [], recipe, { amount: -220 }, true, "PINNED");
        if (!up.ok || up.updatedCount !== 1) { console.error("FAIL r87 update: " + JSON.stringify(up)); process.exit(4); }
        const after = ctrl.property(1).value;
        if (Math.abs(after - (-220)) > 0.0001) { console.error("FAIL r87: master value " + after); process.exit(5); }
        if (Math.abs(before - after) < 0.0001) { console.error("FAIL r87: value unchanged"); process.exit(6); }
        // per-layer controls must never exist on the target layer in master mode
        if (f.effects.numProperties !== 1) { console.error("FAIL r87: per-layer controls appeared"); process.exit(7); }
        if (f.thr.expression === "") { console.error("FAIL r87: pinned expression lost"); process.exit(8); }
        console.log("PASS: R87 PINNED + Shared Master updates master controls.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R87 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r88_pinned_perlayer_update_changes_targetlayer_controls_only(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap.ok) { console.error("FAIL r88 apply: " + JSON.stringify(ap)); process.exit(1); }
        if (global.vac34_ControllerManager.findMasterLayer(f.comp)) { console.error("FAIL r88: master created unexpectedly"); process.exit(2); }
        const fx = f.effects.property(global.vac34_ControllerManager.getEffectPrefixForRecipe(recipe) + " \\u2014 Amount %%");
        if (!fx) { console.error("FAIL r88: per-layer control missing"); process.exit(3); }
        const up = global.vac34_Engine.updateParameters(f.comp, [], recipe, { amount: 140 }, false, "PINNED");
        if (!up.ok || up.updatedCount !== 1) { console.error("FAIL r88 update: " + JSON.stringify(up)); process.exit(4); }
        if (Math.abs(fx.property(1).value - 140) > 0.0001) { console.error("FAIL r88 value"); process.exit(5); }
        console.log("PASS: R88 PINNED + Per-Layer updates target-layer controls.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R88 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r89_update_no_false_success_on_wrong_owner(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap.ok) { console.error("FAIL r89 apply"); process.exit(1); }
        const fx = f.effects.property(global.vac34_ControllerManager.getEffectPrefixForRecipe(recipe) + " \\u2014 Amount %%");
        const before = fx.property(1).value;
        // rig is Per-Layer; a Shared-Master update must not silently claim success
        const up = global.vac34_Engine.updateParameters(f.comp, [], recipe, { amount: 999 }, true, "PINNED");
        if (up.ok || up.status !== "CONTROLLER_MISSING" || up.updatedCount !== 0) {
            console.error("FAIL r89: " + JSON.stringify(up)); process.exit(2);
        }
        if (Math.abs(fx.property(1).value - before) > 0.0001) { console.error("FAIL r89: wrong owner was modified"); process.exit(3); }
        if (global.vac34_ControllerManager.findMasterLayer(f.comp)) { console.error("FAIL r89: update invented a master null"); process.exit(4); }
        console.log("PASS: R89 wrong controller owner never reports success.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R89 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE C — remove controller lifecycle
    # ------------------------------------------------------------------
    def test_r90_pinned_remove_cleans_unreferenced_controls(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap.ok) { console.error("FAIL r90 apply"); process.exit(1); }
        if (f.effects.numProperties !== 8) { console.error("FAIL r90 setup controls: " + f.effects.numProperties); process.exit(2); }
        const rm = global.vac34_Engine.removeRecipe(f.comp, [], recipe, null, "PINNED");
        if (!rm.ok || rm.removedCount !== 1) { console.error("FAIL r90: " + JSON.stringify(rm)); process.exit(3); }
        if (rm.controlsRemoved < 1) { console.error("FAIL r90: no controls cleaned: " + JSON.stringify(rm)); process.exit(4); }
        if (f.effects.numProperties !== 1) { console.error("FAIL r90 orphans: " + f.effects.numProperties); process.exit(5); }
        if (f.thr.expression !== "") { console.error("FAIL r90 expression"); process.exit(6); }
        console.log("PASS: R90 PINNED remove cleans unreferenced owned controls.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R90 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r91_pinned_remove_preserves_shared_controls_with_consumers(self):
        code = """
        const f = mkPinnedComp();
        // second consumer layer with its own 1D slider property
        const sExpr = [];
        const slider = { name: "Amount", matchName: "ADBE Slider Control", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true, value: 0,
            get expression() { return sExpr[0]; }, set expression(v) { sExpr[0] = v; } };
        const l2fx = effectsGroupMock();
        const sHandle = l2fx.addProperty("ADBE Slider Control", "consumer slider", slider);
        slider.parentProperty = sHandle; sHandle.parentProperty = l2fx;
        const l2 = { name: "Other Layer", comment: "", selectedProperties: [slider],
            property(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? l2fx : null; } };
        l2fx.parentProperty = l2;
        f.layers.push(l2);
        f.comp.selectedProperties = [slider];
        global.app.project.numItems = 1;

        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap1 = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, true, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap1.ok) { console.error("FAIL r91 apply1: " + JSON.stringify(ap1)); process.exit(1); }
        const master = global.vac34_ControllerManager.findMasterLayer(f.comp);
        const mfx = master.property("ADBE Effect Parade");
        const ctrlName = global.vac34_ControllerManager.getEffectPrefixForRecipe(recipe) + " \\u2014 Amount %%";
        if (!mfx.property(ctrlName)) { console.error("FAIL r91: master control missing"); process.exit(2); }
        // second consumer on the OTHER layer, shared master
        const ap2 = global.vac34_Engine.applyRecipe(f.comp, [l2], recipe, pVals, true, "Audio Amplitude", "Both Channels", "SELECTED_PROPERTY");
        if (!ap2.ok) { console.error("FAIL r91 apply2: " + JSON.stringify(ap2)); process.exit(3); }
        if (slider.expression === "") { console.error("FAIL r91: consumer expression missing"); process.exit(4); }
        // remove only the pinned rig
        const rm = global.vac34_Engine.removeRecipe(f.comp, [], recipe, null, "PINNED");
        if (!rm.ok || rm.removedCount !== 1) { console.error("FAIL r91 remove: " + JSON.stringify(rm)); process.exit(5); }
        if (rm.controlsRemoved !== 0) { console.error("FAIL r91: shared controls removed while in use: " + rm.controlsRemoved); process.exit(6); }
        if (!mfx.property(ctrlName)) { console.error("FAIL r91: master control vanished"); process.exit(7); }
        if (slider.expression === "") { console.error("FAIL r91: other consumer expression killed"); process.exit(8); }
        console.log("PASS: R91 shared master controls preserved for remaining consumer.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R91 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r92_remove_never_deletes_unrelated_effects(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (!ap.ok) { console.error("FAIL r92 apply"); process.exit(1); }
        const foreignFx = f.effects.addProperty("ADBE Radial Blur", "Radial Blur", { name: "Amount" });
        const foreignSlider = f.effects.property("Radial Blur");
        const rm = global.vac34_Engine.removeRecipe(f.comp, [], recipe, null, "PINNED");
        if (!rm.ok) { console.error("FAIL r92 remove: " + JSON.stringify(rm)); process.exit(2); }
        if (!foreignSlider) { console.error("FAIL r92: foreign effect deleted"); process.exit(3); }
        // Glow effect + foreign effect survive; all 7 controllers are gone
        if (f.effects.numProperties !== 2) { console.error("FAIL r92: final effect count " + f.effects.numProperties); process.exit(4); }
        console.log("PASS: R92 unrelated foreign effects survive remove.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R92 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r93_repeated_apply_remove_no_orphan_accumulation(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        for (let cycle = 0; cycle < 3; cycle++) {
            const ap = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
            if (!ap.ok || ap.status !== "APPLIED_VERIFIED") { console.error("FAIL r93 cycle " + cycle + " apply: " + JSON.stringify(ap)); process.exit(1); }
            const rm = global.vac34_Engine.removeRecipe(f.comp, [], recipe, null, "PINNED");
            if (!rm.ok || rm.removedCount !== 1) { console.error("FAIL r93 cycle " + cycle + " remove: " + JSON.stringify(rm)); process.exit(2); }
            if (f.effects.numProperties !== 1) { console.error("FAIL r93 orphans after cycle " + cycle + ": " + f.effects.numProperties); process.exit(3); }
            if (f.thr.expression !== "") { console.error("FAIL r93 expr"); process.exit(4); }
        }
        if (f.lyr.comment.indexOf("[vac34_rig:") !== -1) { console.error("FAIL r93: stale rig tag left in comment"); process.exit(5); }
        console.log("PASS: R93 repeated Apply/Remove leaves no orphan controls.");
        process.exit(0);
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R93 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE D — UI geometry (mock tier; real AE viewport is WAVE H/host)
    # ------------------------------------------------------------------
    def test_r94_narrow_panel_action_buttons(self):
        code = """
        global.app = { project: { activeItem: null } };
        installScriptUiMock([220, 260]);
        const win = global.vac34_UIBuilder.build(null);
        if (!win) { console.error("FAIL r94 build"); process.exit(1); }
        function findAll(el, pred, acc) {
            if (pred(el)) acc.push(el);
            (el.children || []).forEach(function(c) { findAll(c, pred, acc); });
            return acc;
        }
        const btns = findAll(win, function(e) { return e.type === "button"; }, []);
        const wanted = {};
        wanted["\\u25B6 Apply"] = false; wanted["Update"] = false; wanted["Remove"] = false;
        btns.forEach(function(b) { if (Object.prototype.hasOwnProperty.call(wanted, b.text)) wanted[b.text] = true; });
        const missing = Object.keys(wanted).filter(function(k) { return !wanted[k]; });
        if (missing.length) { console.error("FAIL r94 missing buttons: " + missing.join(",")); process.exit(1); }
        const allWired = btns.every(function(b) { return typeof b.onClick === "function" && b.enabled !== false; });
        if (!allWired) { console.error("FAIL r94 unwired/disabled button"); process.exit(2); }
        const statusText = win.getStatusText();
        if (typeof statusText !== "string" || statusText === "") { console.error("FAIL r94 status box"); process.exit(3); }
        console.log("PASS: R94 narrow panel keeps wired action buttons and status.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R94 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r95_real_ae_scroll_viewport(self):
        self.skipTest(
            "NOT_RUN: R95 requires a real After Effects 2024 docked ScriptUI "
            "viewport to prove clipping/scrolling (Wave D host geometry)."
        )

    def test_r96_recipe_change_recomputes_scroll_geometry(self):
        code = """
        global.app = { project: { activeItem: null } };
        installScriptUiMock([260, 380]);
        const win = global.vac34_UIBuilder.build(null);
        win.getHeaderGroup().size = [240, 46];
        win.getFooterGroup().size = [240, 74];
        win.getContentGroup().size = [240, 460];
        win.refreshLayout(true);
        const maxA = win.getScrollbar().maximum;
        if (maxA <= 0) { console.error("FAIL r96: no scroll range"); process.exit(1); }
        win.setAuthoritativeSelection(global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing"));
        win.getContentGroup().size = [240, 300];
        win.refreshLayout(true);
        const maxB = win.getScrollbar().maximum;
        if (maxB >= maxA) { console.error("FAIL r96: scroll not recomputed " + maxA + " -> " + maxB); process.exit(2); }
        const loc = win.getViewportGroup().location;
        if (loc[1] !== 10 + 46 + 6) { console.error("FAIL r96: viewport top drifted: " + JSON.stringify(loc)); process.exit(3); }
        console.log("PASS: R96 recipe change recomputes scroll geometry.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R96 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE E — audio source identity
    # ------------------------------------------------------------------
    def test_r97_audio_source_identity_survives_refresh(self):
        code = """
        const f = mkPinnedComp();
        installScriptUiMock([320, 420]);
        const win = global.vac34_UIBuilder.build(null);
        // sole verified source: auto-selected once, never re-selected by accident
        const idxBefore = (win.getAudioStatusLabel().text === "AUDIO READY");
        if (!idxBefore) { console.error("FAIL r97: ready label expected, got " + win.getAudioStatusLabel().text); process.exit(1); }
        win.refreshCompStatus();
        const label = win.getAudioStatusLabel().text;
        if (label !== "AUDIO READY") { console.error("FAIL r97: relink broke audio state: " + label); process.exit(2); }
        // an explicit user selection must survive a refresh unchanged
        const drop = findDropdown(win, "audioLayerDrop");
        drop.selection = 0;
        drop.onChange();
        win.refreshCompStatus();
        if (drop.selection === null) { console.error("FAIL r97: identity not restored after refresh"); process.exit(3); }
        console.log("PASS: R97 audio identity survives refresh.");
        process.exit(0);
        function findDropdown(root, key) {
            // dropdowns created in build order: target, category, audio layer, audio channel
            function collect(el, acc) {
                if (el.type === "dropdownlist") acc.push(el);
                (el.children || []).forEach(function(c) { collect(c, acc); });
                return acc;
            }
            const all = collect(root, []);
            return all[2];
        }
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R97 failed:\n{proc.stderr}\n{proc.stdout}")

    def test_r98_duplicate_audio_names_never_silently_relink(self):
        code = """
        // two layers sharing the display name "Audio Amplitude"
        const f = mkPinnedComp();
        const afx = effectsGroupMock();
        afx.addProperty("ADBE Slider Control", "Both Channels", { name: "Slider" });
        const dup = { name: "Audio Amplitude", comment: "",
            property(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? afx : null; } };
        afx.parentProperty = dup;
        f.layers.push(dup);
        global.app.project.activeItem = f.comp;
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const recipe = %s;
        const pVals = { math_mode: 0, amount: 100, output_min: 0, output_max: -35, audio_threshold: 0, input_max: 30, smoothing: 3 };
        const res = global.vac34_Engine.applyRecipe(f.comp, [], recipe, pVals, false, "Audio Amplitude", "Both Channels", "PINNED");
        if (res.ok || res.status !== "AUDIO_MISSING") { console.error("FAIL r98 engine: " + JSON.stringify(res)); process.exit(1); }
        if (res.message.indexOf("ambiguous") === -1) { console.error("FAIL r98 message: " + res.message); process.exit(2); }
        if (f.thr.expression !== "") { console.error("FAIL r98: expression written anyway"); process.exit(3); }
        // UI layer: nothing is silently selected as the audio source
        installScriptUiMock([320, 420]);
        const drop = findDropdownPair(global.vac34_UIBuilder.build(null));
        if (drop.selection !== null) { console.error("FAIL r98: dropdown silently picked a source"); process.exit(4); }
        console.log("PASS: R98 duplicate audio names never silently relink.");
        process.exit(0);
        function findDropdownPair(win) {
            function collect(el, acc) {
                if (el.type === "dropdownlist") acc.push(el);
                (el.children || []).forEach(function(c) { collect(c, acc); });
                return acc;
            }
            return collect(win, [])[2];
        }
        """ % audio_recipe_getter()
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R98 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE F — context stability
    # ------------------------------------------------------------------
    def test_r99_focus_change_does_not_retarget_pinned_property(self):
        code = """
        const f = mkPinnedComp();
        global.vac34_AEDom.pinTarget(f.comp, f.thr);
        const other = { name: "OtherComp", numLayers: 0, selectedLayers: [],
            layer: function() { return null; } };
        global.app.project.activeItem = other;
        global.app.project.numItems = 2;
        let call = 0;
        global.app.project.item = function(i) { call++; return (i === 1) ? f.comp : other; };
        const res = global.vac34_AEDom.resolvePinnedTarget();
        if (!res.ok || res.prop !== f.thr) { console.error("FAIL r99: " + JSON.stringify(res)); process.exit(1); }
        console.log("PASS: R99 viewer focus change does not retarget pinned property.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, f"R99 failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE G — test infrastructure
    # ------------------------------------------------------------------
    def test_r100_portable_tests_never_require_personal_windows_paths(self):
        """R100: any personal-drive/deployment path in the portable suite is gated."""
        unit_dir = os.path.join(WORKSPACE_ROOT, "tests", "unit")
        offenders = []
        for path in sorted(glob.glob(os.path.join(unit_dir, "test_*.py"))):
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            guarded = ("os.path.exists" in text) or ("skipTest" in text)
            if ("MIRROR_INSTALL_DIR" in text or "V:\\__STORE_V" in text or "V:/__STORE_V" in text) and not guarded:
                offenders.append(os.path.basename(path))
        self.assertEqual(offenders, [], f"Unguarded personal-path readers: {offenders}")

    def test_r101_clean_archive_rebuild_independent_of_live_deployment(self):
        """R101: clean ZIP rebuild must not depend on the live deployment env."""
        if os.environ.get("VAC34_EXPORTING") == "1":
            self.skipTest("Skipping nested export during export verification")
        manage_script = os.path.join(WORKSPACE_ROOT, "scripts", "manage.py")
        env = dict(os.environ)
        env["VAC34_EXPORTING"] = "1"
        # A temp HOME keeps the nested run from touching user state.
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_home:
            env["HOME"] = tmp_home
            env["USERPROFILE"] = tmp_home
            proc = subprocess.run([sys.executable, manage_script, "export"],
                                  cwd=WORKSPACE_ROOT, capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, f"R101 clean export failed:\n{proc.stderr}\n{proc.stdout}")
        self.assertIn("Definitive verification complete: PASS", proc.stdout)

    def test_r102_real_windows_deployment_hashes(self):
        """R102 (gated): real Live/Mirror hashes via scripts/manage.py verify."""
        if os.environ.get("VAC34_DEPLOYMENT_CHECK") != "1":
            self.skipTest("NOT_RUN: R102 requires opt-in deployment check on this Windows machine "
                          "(VAC34_DEPLOYMENT_CHECK=1 python scripts/manage.py verify).")
        manage_script = os.path.join(WORKSPACE_ROOT, "scripts", "manage.py")
        proc = subprocess.run([sys.executable, manage_script, "verify"],
                              cwd=WORKSPACE_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"R102 deployment verify failed:\n{proc.stderr}\n{proc.stdout}")

    # ------------------------------------------------------------------
    # WAVE H — real AE host acceptance (cannot run without AE 2024)
    # ------------------------------------------------------------------
    def test_r104_glow_threshold_audio_mapping_real_ae(self):
        self.skipTest(
            "NOT_RUN: R104 requires After Effects 2024 (Glow Threshold reactivity). "
            "Run tests/ae_runtime/host_smoke_test.jsx in the AE host (Wave H)."
        )

    def test_r105_shared_master_rig_survives_save_reopen(self):
        self.skipTest(
            "NOT_RUN: R105 requires real project save/reopen in After Effects 2024."
        )


if __name__ == "__main__":
    unittest.main()
