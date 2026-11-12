/**
 * vac34_AE — Master Expressions Studio
 * Version 0.0.1
 * Entry Point
 */

try {
    if (typeof vac34_UIBuilder !== "undefined") {
        // Reentry guard: re-running the script into an already-built panel must
        // not accumulate controls or re-run the initial layout resize twice.
        // The panel owns its manual geometry (fixed header/footer + bounded
        // scroll viewport), so a re-run only refreshes, never re-lays out.
        var ui = vac34_UIBuilder.build(thisObj);
        if (ui) {
            if (typeof ui.refreshLayout === "function") {
                ui.refreshLayout(true);
            }
            if (typeof Window !== "undefined" && (ui instanceof Window)) {
                ui.center();
                ui.show();
            }
        }
    }
} catch (e) {
    var stage = (typeof vac34_Diagnostics !== "undefined") ? vac34_Diagnostics.getCurrentStartupStage() : "Startup";
    if (thisObj && typeof thisObj === "object" && thisObj.layout) {
        try {
            thisObj.layout.layout(true);
            thisObj.layout.resize();
        } catch (layErr) {}
    }
    if (typeof alert !== "undefined") {
        alert("vac34_AE Initialization Error [" + stage + "]: " + (e.message || e) + (e.line ? ("\nLine: " + e.line) : ""));
    }
}
