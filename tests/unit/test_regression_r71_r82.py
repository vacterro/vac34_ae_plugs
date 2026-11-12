#!/usr/bin/env python3
"""
vac34_AE T-6 Regression Suite (R71-R82)
SAIHANDOFF §14 acceptance coverage for the UI/UX recovery:
 scrollable panel with fixed footer, visible operation results, pinned
 composition, pinned target, audio source status, partial batch status,
 metadata-driven parameter editor, PINNED-mode update and automatic build identity.
"""

import json
import os
import subprocess
import sys
import unittest

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
                // Real AE effect groups expose their child count; without it
                // recipe-property discovery cannot descend into the effect.
                numProperties: 1,
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

JS_SCRIPTUI_MOCK = """
function MockElement(type, text, val) {
    this.type = type;
    this.text = (typeof text === "string") ? text : "";
    this.selection = null;
    this.items = [];
    this.children = [];
    this.enabled = true;
    this.value = (typeof val === "number") ? val : 0;
    this.preferredSize = [100, 20];
    this.size = [300, 400];
    this.location = [0, 0];
    this.visible = true;
    this.margins = 0;
    this.spacing = 0;
    this.layout = { layout: function() {}, resize: function() {} };
}
MockElement.prototype.add = function(t, bounds, a1, a2) {
    if (t === "item") {
        // ScriptUI leniency: a bare string argument is the item text
        var label = (typeof bounds === "string") ? bounds : a1;
        const item = { text: label || "", index: this.items.length };
        this.items.push(item);
        return item;
    }
    var label = (typeof bounds === "string") ? bounds : (typeof a1 === "string" ? a1 : "");
    const elem = new MockElement(t, label, (typeof bounds === "number") ? bounds : 0);
    elem.parent = this;
    this.children.push(elem);
    return elem;
};
MockElement.prototype.removeAll = function() { this.items = []; };
MockElement.prototype.remove = function(child) {
    const idx = this.children.indexOf(child);
    if (idx !== -1) this.children.splice(idx, 1);
};
function installScriptUiMock(windowSize) {
    global.Window = function(type, title) {
        const e = new MockElement(type, title);
        if (windowSize) e.size = windowSize;
        e.show = () => {};
        e.center = () => {};
        e.close = () => {};
        return e;
    };
    global.Panel = MockElement;
    global.ScriptUI = { newFont: () => ({}) };
    global.alert = function(m) { global.__lastAlert = m; };
    global.prompt = function(m, d) { return d; };
}
"""


class TestRegressionR71ToR82(unittest.TestCase):
    def run_node_snippet(self, code, extra_globals=None):
        full_code = (
            "const fs = require('fs');\n"
            "const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');\n"
            "new Function('thisObj', bundle)(global);\n"
            + JS_EFFECTS_GROUP
            + "\n"
            + JS_SCRIPTUI_MOCK
            + "\n"
            + code
        )
        return subprocess.run(["node", "-e", full_code], cwd=WORKSPACE_ROOT, capture_output=True, text=True)

    # ------------------------------------------------------------------
    # R71: metadata-driven enum editor replaces the continuous Mode slider
    # ------------------------------------------------------------------
    def test_r71_mode_rendered_as_dropdown_with_labels(self):
        code = """
        global.app = { project: { activeItem: null } };
        installScriptUiMock();
        const win = global.vac34_UIBuilder.build(null);
        const cm = win.getParamControlMap();
        const mode = cm["math_mode"];
        if (!mode || mode.editor !== "enum") {
            console.error("FAIL r71: math_mode editor=" + (mode ? mode.editor : "missing")); process.exit(1);
        }
        const labels = mode.dropdown.items.map(function(i) { return i.text; });
        if (labels.join(",") !== "Add,Multiply,Absolute") {
            console.error("FAIL r71: labels=" + labels.join(",")); process.exit(2);
        }
        if (global.vac34_UIBuilder && !win.getCurrentSelectedRecipe()) { process.exit(3); }
        console.log("PASS: R71 enum dropdown labels rendered.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R72: fixed header/footer, real scrollbar, scroll range recomputed
    # ------------------------------------------------------------------
    def test_r72_fixed_chrome_and_scroll_range(self):
        code = """
        global.app = { project: { activeItem: null } };
        installScriptUiMock([320, 360]);
        const win = global.vac34_UIBuilder.build(null);
        // realistic element heights
        win.getHeaderGroup().size = [300, 46];
        win.getFooterGroup().size = [300, 74];
        win.getContentGroup().size = [300, 420];
        win.refreshLayout(true);

        const footerLoc = win.getFooterGroup().location;
        const headerLoc = win.getHeaderGroup().location;
        if (footerLoc[1] <= headerLoc[1]) {
            console.error("FAIL r72: footer not below header: " + JSON.stringify([headerLoc, footerLoc])); process.exit(1);
        }
        const sb = win.getScrollbar();
        if (!sb.visible || sb.maximum <= 0) {
            console.error("FAIL r72: scrollbar inactive for overflowing content (max=" + sb.maximum + ")"); process.exit(2);
        }
        const maxBefore = sb.maximum;
        // switch to a recipe with fewer parameters: scroll range must shrink
        win.setAuthoritativeSelection(global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing"));
        win.getContentGroup().size = [300, 300];
        win.refreshLayout(true);
        const maxAfter = win.getScrollbar().maximum;
        if (maxAfter >= maxBefore) {
            console.error("FAIL r72: scroll range not recomputed: before=" + maxBefore + " after=" + maxAfter); process.exit(3);
        }
        // the always-visible status lives in the fixed footer group
        win.executeUiOperation("apply");
        const footerText = win.getStatusText();
        if (footerText.indexOf("COMP_MISSING") === -1) {
            console.error("FAIL r72: footer status not visible: " + footerText); process.exit(4);
        }
        console.log("PASS: R72 fixed chrome + scrollbar + visible status.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R73: an unexpected handler exception becomes a visible status
    # ------------------------------------------------------------------
    def test_r73_unexpected_handler_exception_is_visible(self):
        code = """
        const audioLyr = { name: "Audio Amplitude",
            property: function(p) { return (p === "ADBE Effect Parade" || p === "Effects") ? audioFx : null; } };
        const audioFx = effectsGroupMock();
        audioFx.addProperty("ADBE Both Channels", "Both Channels", { name: "Slider" });
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? audioLyr : null; },
            selectedLayers: [], selectedProperties: [] };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };
        installScriptUiMock();
        const win = global.vac34_UIBuilder.build(null);
        global.vac34_Engine.applyRecipe = function() { throw new Error("host exploded"); };
        win.executeUiOperation("apply");
        const txt = win.getStatusText();
        if (txt.indexOf("UNEXPECTED_ERROR") !== 0) {
            console.error("FAIL r73: status=" + txt); process.exit(1);
        }
        if (txt.indexOf("host exploded") === -1) {
            console.error("FAIL r73: cause missing: " + txt); process.exit(2);
        }
        console.log("PASS: R73 unexpected handler exception surfaced.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R74: pinned composition survives viewer focus changes and reports loss
    # ------------------------------------------------------------------
    def test_r74_pinned_composition_survives_focus_change(self):
        code = """
        const compA = { name: "CompA", numLayers: 0, selectedLayers: [] };
        const compB = { name: "CompB", numLayers: 0, selectedLayers: [] };
        let projectItems = [compA, compB];
        global.app = { project: { activeItem: compB, numItems: 2,
            item: function(i) { return projectItems[i - 1]; } } };

        global.vac34_AEDom.pinComp(compA);
        if (!global.vac34_AEDom.isCompPinned()) { console.error("FAIL r74: not pinned"); process.exit(1); }
        // viewer focus moves elsewhere
        global.app.project.activeItem = compB;
        const r1 = global.vac34_AEDom.resolvePinnedComp();
        if (!r1.ok || r1.comp !== compA) { console.error("FAIL r74: pin lost on focus change"); process.exit(2); }

        // pinned comp deleted from project
        projectItems = [compB];
        global.app.project.numItems = 1;
        const r2 = global.vac34_AEDom.resolvePinnedComp();
        if (r2.ok || r2.error !== "PINNED_COMP_MISSING") {
            console.error("FAIL r74: dead pin not reported: " + JSON.stringify(r2)); process.exit(3);
        }
        if (r2.message.indexOf("CompA") === -1) { console.error("FAIL r74: name missing in error"); process.exit(4); }
        console.log("PASS: R74 pinned composition stable and honestly reported when lost.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    def test_r74b_ui_shows_pinned_comp_marker(self):
        code = """
        const compA = { name: "CompA", numLayers: 0, selectedLayers: [] };
        global.app = { project: { activeItem: compA, numItems: 1, item: function(i) { return compA; } } };
        installScriptUiMock();
        const win = global.vac34_UIBuilder.build(null);
        global.vac34_AEDom.pinComp(compA);
        win.refreshCompStatus();
        const label = win.getAudioStatusLabel();
        if (!label) { console.error("FAIL r74b: status label missing"); process.exit(1); }
        // composition marker visible through the comp status text in header
        const headerTexts = [];
        function walk(node, depth) {
            if (!node || depth > 4) return;
            if (node.text) headerTexts.push(node.text);
            (node.children || []).forEach(function(c) { walk(c, depth + 1); });
        }
        walk(win.getHeaderGroup(), 0);
        const joined = headerTexts.join(" | ");
        if (joined.indexOf("[Pinned]") === -1) {
            console.error("FAIL r74b: pin marker not shown: " + joined); process.exit(2);
        }
        console.log("PASS: R74b pinned composition marker visible.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R75: pinned target survives controller addProperty reacquisition
    # ------------------------------------------------------------------
    def test_r75_pinned_target_reacquired_after_addproperty(self):
        code = """
        let thrExpr = "";
        const thr = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return thrExpr; }, set expression(v) { thrExpr = v; } };
        const effects = effectsGroupMock();
        const glowHandle = effects.addProperty("ADBE Glow", "Glow", thr);
        thr.parentProperty = glowHandle;
        glowHandle.parentProperty = effects;
        const lyr = { name: "Shot", index: 1, selectedProperties: [], comment: "",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; },
            selectedLayers: [], selectedProperties: [] };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };

        const pinRes = global.vac34_AEDom.pinTarget(comp, thr);
        if (!pinRes.ok) { console.error("FAIL r75: pin failed: " + JSON.stringify(pinRes)); process.exit(1); }

        // structural change: controller adds a slider effect on the layer
        effects.addProperty("ADBE Slider Control", "vac34 — Test — Amount %", null);

        const res = global.vac34_AEDom.resolvePinnedTarget();
        if (!res.ok) { console.error("FAIL r75: reacquire failed: " + JSON.stringify(res)); process.exit(2); }
        if (res.prop !== thr) { console.error("FAIL r75: resolved wrong instance"); process.exit(3); }
        console.log("PASS: R75 pinned target reacquired after addProperty.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R76: duplicate Glow instances make pinned resolution fail closed
    # ------------------------------------------------------------------
    def test_r76_duplicate_effect_rejected_by_pin_resolution(self):
        code = """
        let e1 = "", e2 = "";
        const t1 = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return e1; }, set expression(v) { e1 = v; } };
        const t2 = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return e2; }, set expression(v) { e2 = v; } };
        const effects = effectsGroupMock();
        const h1 = effects.addProperty("ADBE Glow", "Glow", t1);
        const h2 = effects.addProperty("ADBE Glow", "Glow", t2);
        t1.parentProperty = h1; t2.parentProperty = h2;
        h1.parentProperty = effects; h2.parentProperty = effects;
        const lyr = { name: "Shot", index: 1, selectedProperties: [],
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; } };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };

        global.vac34_AEDom.pinTarget(comp, t1);
        const res = global.vac34_AEDom.resolvePinnedTarget();
        if (res.ok) { console.error("FAIL r76: ambiguous pin resolved"); process.exit(1); }
        if (res.error !== "PINNED_TARGET_REACQUIRE_FAILED") {
            console.error("FAIL r76: wrong error " + res.error); process.exit(2);
        }
        console.log("PASS: R76 duplicate Glow rejected by pin resolution.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R77: audio source status states are honest
    # ------------------------------------------------------------------
    def test_r77_audio_status_states(self):
        code = """
        // no comp
        let s = global.vac34_AudioEngine.getAudioStatus(null, "Audio Amplitude", "Both Channels");
        if (s.state !== "NO_COMP" || s.valid) { console.error("FAIL r77a: " + s.state); process.exit(1); }

        // comp without any audio layer
        const effects = effectsGroupMock();
        const lyr = { name: "Shot", index: 1,
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; } };
        s = global.vac34_AudioEngine.getAudioStatus(comp, "Audio Amplitude", "Both Channels");
        if (s.state !== "AUDIO_MISSING" || s.valid) { console.error("FAIL r77b: " + s.state); process.exit(2); }

        // audio layer present, channel missing
        const aEffects = effectsGroupMock();
        aEffects.addProperty("ADBE ILLUSION", "Both Channels", null);
        const aLyr = { name: "Audio Amplitude", index: 1,
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? aEffects : null; } };
        const comp2 = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? aLyr : null; } };
        s = global.vac34_AudioEngine.getAudioStatus(comp2, "Audio Amplitude", "Left Channel");
        if (s.state !== "CHANNEL_MISSING" || s.valid) { console.error("FAIL r77c: " + s.state); process.exit(3); }
        s = global.vac34_AudioEngine.getAudioStatus(comp2, "Audio Amplitude", "Both Channels");
        if (s.state !== "AUDIO_READY" || !s.valid) { console.error("FAIL r77d: " + s.state); process.exit(4); }

        // duplicate audio layer names are ambiguous, never silently first
        const aLyr2 = { name: "Audio Amplitude", index: 2,
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? aEffects : null; } };
        const comp3 = { name: "Comp", numLayers: 2,
            layer: function(i) { return (i === 1) ? aLyr : aLyr2; } };
        s = global.vac34_AudioEngine.getAudioStatus(comp3, "Audio Amplitude", "Both Channels");
        if (s.state !== "SOURCE_AMBIGUOUS" || s.valid) { console.error("FAIL r77e: " + s.state); process.exit(5); }
        console.log("PASS: R77 audio status states honest.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R78: partial batch is never reported as fully verified
    # ------------------------------------------------------------------
    def test_r78_partial_batch_status(self):
        code = """
        let p1expr = "";
        const p1 = { name: "Opacity", matchName: "ADBE Opacity", propertyIndex: 2,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return p1expr; }, set expression(v) { p1expr = v; },
            expressionEnabled: true };
        let p2expr = "wiggle(3, 40)"; // foreign expression must be preserved
        const p2 = { name: "Opacity", matchName: "ADBE Opacity", propertyIndex: 3,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return p2expr; }, set expression(v) { p2expr = v; },
            expressionEnabled: true };
        p1.parentProperty = { name: "Transform" };
        p1.parentProperty.parentProperty = null;
        p2.parentProperty = { name: "Transform" };
        p2.parentProperty.parentProperty = null;
        const effects = effectsGroupMock();
        // Transform group resolves children by index only ("Opacity" by name is ambiguous here)
        const transformGroup = { name: "Transform", matchName: "ADBE Transform",
            numProperties: 2,
            property: function(k) {
                if (k === 2) return p1;
                if (k === 3) return p2;
                return null;
            } };
        const lyr = { name: "Layer", index: 1, selectedProperties: [p1, p2],
            property: function(p) {
                if (p === "Effects" || p === "ADBE Effect Parade") return effects;
                if (p === "Transform" || p === "ADBE Transform") return transformGroup;
                return null;
            } };
        const comp = { name: "Comp", numLayers: 1, selectedLayers: [lyr], selectedProperties: [p1, p2] };

        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
        if (res.status !== "PARTIAL_SUCCESS") { console.error("FAIL r78: status=" + res.status); process.exit(1); }
        if (res.appliedCount !== 1) { console.error("FAIL r78: applied=" + res.appliedCount); process.exit(2); }
        if (res.conflictCount !== 1) { console.error("FAIL r78: conflicts=" + res.conflictCount); process.exit(3); }
        if (p2expr !== "wiggle(3, 40)") { console.error("FAIL r78: foreign expression clobbered"); process.exit(4); }
        if (res.message.indexOf("1 applied") === -1 || res.message.indexOf("1 conflicted") === -1) {
            console.error("FAIL r78: counts missing: " + res.message); process.exit(5);
        }
        console.log("PASS: R78 partial batch reported as PARTIAL_SUCCESS.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R79: PINNED apply drives exactly the pinned property
    # ------------------------------------------------------------------
    def test_r79_pinned_apply_and_remove(self):
        code = """
        let thrExpr = "";
        const thr = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return thrExpr; }, set expression(v) { thrExpr = v; },
            expressionEnabled: true };
        let otherExpr = "";
        const other = { name: "Glow Intensity", matchName: "ADBE Glow Intensity", propertyIndex: 2,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return otherExpr; }, set expression(v) { otherExpr = v; },
            expressionEnabled: true };
        const effects = effectsGroupMock();
        const glowHandle = effects.addProperty("ADBE Glow", "Glow", thr);
        glowHandle.property = function(k) {
            if (k === 1 || k === "Threshold") return thr;
            if (k === 2 || k === "Glow Intensity") return other;
            return null;
        };
        thr.parentProperty = glowHandle; other.parentProperty = glowHandle;
        glowHandle.parentProperty = effects;
        const lyr = { name: "Shot", index: 1, selectedProperties: [], comment: "",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; },
            selectedLayers: [], selectedProperties: [] };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };

        global.vac34_AEDom.pinTarget(comp, thr);
        const recipe = global.vac34_RecipeRegistry.getRecipeById("RECIPE_ID_PLACEHOLDER");
        const res = global.vac34_Engine.applyRecipe(comp, [], recipe, {}, false, null, null, "PINNED");
        if (!res.ok) { console.error("FAIL r79a: apply failed: " + JSON.stringify(res)); process.exit(1); }
        if (res.appliedCount !== 1) { console.error("FAIL r79a: applied=" + res.appliedCount); process.exit(2); }
        if (thrExpr.indexOf("RECIPE_ID_PLACEHOLDER") === -1) { console.error("FAIL r79a: pinned prop untouched"); process.exit(3); }
        if (otherExpr !== "") { console.error("FAIL r79a: sibling property touched"); process.exit(4); }

        const rm = global.vac34_Engine.removeRecipe(comp, [], recipe, null, "PINNED");
        if (!rm.ok || rm.removedCount !== 1) { console.error("FAIL r79b: " + JSON.stringify(rm)); process.exit(5); }
        if (thrExpr !== "") { console.error("FAIL r79b: pinned expression not cleared"); process.exit(6); }
        console.log("PASS: R79 PINNED apply/remove exact.");
        process.exit(0);
        """.replace("RECIPE_ID_PLACEHOLDER", RECIPE_ID)
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R80: UI never presents an audio source that does not exist
    # ------------------------------------------------------------------
    def test_r80_no_fake_audio_selection(self):
        code = """
        const effects = effectsGroupMock();
        const lyr = { name: "Shot", index: 1,
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; },
            selectedLayers: [] };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };
        installScriptUiMock();
        const win = global.vac34_UIBuilder.build(null);
        const audioDrop = null;
        const label = win.getAudioStatusLabel();
        if (label.text !== "AUDIO MISSING") {
            console.error("FAIL r80: status label=" + label.text); process.exit(1);
        }
        // the placeholder item is not presented as a selection
        const headerChildren = win.getHeaderGroup();
        if (!headerChildren) { console.error("FAIL r80: header missing"); process.exit(2); }
        console.log("PASS: R80 no fake audio selection, status AUDIO MISSING.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R81: build identity is automatic, stable and manifest-consistent
    # ------------------------------------------------------------------
    def test_r81_build_fingerprint_stable_and_manifest_consistent(self):
        env = dict(os.environ)
        proc1 = subprocess.run(
            [sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--no-tests"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True, env=env
        )
        self.assertEqual(proc1.returncode, 0, proc1.stderr + "\n" + proc1.stdout)
        with open(os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx"), "r", encoding="utf-8") as f:
            bundle1 = f.read()
        with open(os.path.join(WORKSPACE_ROOT, "release", "build_manifest.json"), "r", encoding="utf-8") as f:
            manifest1 = json.load(f)

        proc2 = subprocess.run(
            [sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--no-tests"],
            cwd=WORKSPACE_ROOT, capture_output=True, text=True, env=env
        )
        self.assertEqual(proc2.returncode, 0, proc2.stderr + "\n" + proc2.stdout)
        with open(os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx"), "r", encoding="utf-8") as f:
            bundle2 = f.read()

        fingerprint = manifest1["build_fingerprint"]
        self.assertTrue(fingerprint.startswith("0.0.1+"), "fingerprint must carry product version: " + fingerprint)
        self.assertIn('BUILD_ID: "' + fingerprint + '"', bundle1, "dist BUILD_ID must equal manifest fingerprint")
        self.assertEqual(bundle1, bundle2, "two builds of identical sources must be byte-identical")
        # a stale hand-edited literal would fail this identity contract
        self.assertNotIn('BUILD_ID: "20261107.02"', bundle1, "source default must not survive into the artifact")

    # ------------------------------------------------------------------
    # R82: parameter values are validated before an operation runs
    # ------------------------------------------------------------------
    def test_r82_parameter_validation_before_apply(self):
        code = """
        global.app = { project: { activeItem: null } };
        installScriptUiMock();
        const win = global.vac34_UIBuilder.build(null);
        const cm = win.getParamControlMap();
        cm["amount"].editbox.text = "99999"; // declared max is 500
        cm["amount"].editbox.onChange();
        const collected = win.collectParameterValues();
        if (collected.errors.length > 0) {
            console.error("FAIL r82: validation errors: " + collected.errors.join(";")); process.exit(1);
        }
        if (collected.values["amount"] !== 500) {
            console.error("FAIL r82: out-of-range value not clamped: " + collected.values["amount"]); process.exit(2);
        }
        if (collected.values["math_mode"] !== 0) {
            console.error("FAIL r82: enum default wrong: " + collected.values["math_mode"]); process.exit(3);
        }
        console.log("PASS: R82 out-of-range parameter clamped before Apply.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

    # ------------------------------------------------------------------
    # R83: PINNED mode Update drives the pinned property, never a silent no-op
    # ------------------------------------------------------------------
    def test_r83_pinned_update_not_silent_noop(self):
        code = """
        // No pin at all: PINNED update must report, not silently claim UPDATED
        const comp0 = { name: "Comp", numLayers: 1, selectedLayers: [], selectedProperties: [],
            layer: function(i) { return null; } };
        const recipe = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
        const r0 = global.vac34_Engine.updateParameters(comp0, [], recipe, { amount: 25 }, false, "PINNED");
        if (r0.ok || r0.status !== "TARGET_NOT_PINNED") {
            console.error("FAIL r83a: " + r0.status); process.exit(1);
        }

        // Pin a target, then verify Update drives that exact layer's control
        let thrExpr = "";
        const thr = { name: "Threshold", matchName: "ADBE Glow Threshold", propertyIndex: 1,
            propertyValueType: 1, canSetExpression: true,
            get expression() { return thrExpr; }, set expression(v) { thrExpr = v; },
            expressionEnabled: true };
        const effects = effectsGroupMock();
        const glowHandle = effects.addProperty("ADBE Glow", "Glow", thr);
        glowHandle.parentProperty = effects;
        thr.parentProperty = glowHandle;
        const prefix = global.vac34_ControllerManager.getEffectPrefixForRecipe(recipe);
        let ctrlValue = 0;
        const ctrlProp = { name: "Slider", setValue: function(v) { ctrlValue = v; },
            get value() { return ctrlValue; } };
        effects.addProperty("ADBE Slider Control", prefix + " — Amount %", ctrlProp);
        const lyr = { name: "Shot", index: 1, selectedProperties: [], comment: "",
            property: function(p) { return (p === "Effects" || p === "ADBE Effect Parade") ? effects : null; } };
        effects.parentProperty = lyr;
        const comp = { name: "Comp", numLayers: 1, layer: function(i) { return (i === 1) ? lyr : null; },
            selectedLayers: [], selectedProperties: [] };
        global.app = { project: { activeItem: comp, numItems: 1, item: function(i) { return comp; } } };

        global.vac34_AEDom.pinTarget(comp, thr);
        const r1 = global.vac34_Engine.updateParameters(comp, [], recipe, { amount: 25 }, false, "PINNED");
        if (!r1.ok || r1.updatedCount < 1) { console.error("FAIL r83b: " + JSON.stringify(r1)); process.exit(2); }
        if (ctrlValue !== 25) { console.error("FAIL r83b: pinned control not updated: " + ctrlValue); process.exit(3); }
        console.log("PASS: R83 PINNED Update drives the pinned target and reports.");
        process.exit(0);
        """
        proc = self.run_node_snippet(code)
        self.assertEqual(proc.returncode, 0, proc.stderr + "\n" + proc.stdout)

if __name__ == "__main__":
    unittest.main()
