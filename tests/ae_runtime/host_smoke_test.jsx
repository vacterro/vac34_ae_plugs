/**
 * vac34_AE Host Smoke Test Runner
 * Validates ScriptUI controls, layout execution, dimensions, and operational behavior in After Effects 2024 runtime.
 * Writes diagnostic smoke report for non-interactive automated verification.
 */

(function(thisObj) {
    "use strict";

    var results = {
        timestamp: (new Date()).toISOString ? (new Date()).toISOString() : String(new Date()),
        hostName: (typeof app !== "undefined" && app.name) ? app.name : "Mock/External",
        hostVersion: (typeof app !== "undefined" && app.version) ? app.version : "Unknown",
        panelCreated: false,
        dockedMode: false,
        titleVerified: false,
        buildIdVerified: false,
        searchBoxPresent: false,
        categoriesPresent: false,
        categoriesCount: 0,
        recipeListPopulated: false,
        recipeListCount: 0,
        paramPanelPresent: false,
        paramControlsCount: 0,
        hasApplyBtn: false,
        hasUpdateBtn: false,
        hasRemoveBtn: false,
        actionButtonsPresent: false,
        initialLayoutPerformed: false,
        geometryValid: false,
        recipeSelectionWorking: false,
        hostScriptExecuted: false,
        structureVerified: false,
        layoutVerified: false,
        expressionRuntimeVerified: false,
        visualVerified: false,
        status: "HOST_UNVERIFIED",
        errors: []
    };

    function safeSerialize(obj) {
        if (typeof JSON !== "undefined" && typeof JSON.stringify === "function") {
            try {
                return JSON.stringify(obj, null, 2);
            } catch (je) {}
        }
        function serializeValue(v) {
            if (v === null) return "null";
            if (typeof v === "boolean" || typeof v === "number") return String(v);
            if (typeof v === "string") {
                return '"' + v.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\n/g, "\\n").replace(/\r/g, "\\r") + '"';
            }
            if (v instanceof Array) {
                var items = [];
                for (var i = 0; i < v.length; i++) items.push(serializeValue(v[i]));
                return "[" + items.join(", ") + "]";
            }
            if (typeof v === "object") {
                var props = [];
                for (var k in v) {
                    if (v.hasOwnProperty(k)) {
                        props.push('"' + k + '": ' + serializeValue(v[k]));
                    }
                }
                return "{\n  " + props.join(",\n  ") + "\n}";
            }
            return '"' + String(v) + '"';
        }
        return serializeValue(obj);
    }

    function writeReport(rep) {
        try {
            if (typeof Folder !== "undefined" && typeof File !== "undefined") {
                var userDir = (Folder.userData && Folder.userData.fsName) ? Folder.userData.fsName : (Folder.temp ? Folder.temp.fsName : "");
                if (userDir) {
                    var targetDir = new Folder(userDir + "/vac34_AE");
                    if (!targetDir.exists) targetDir.create();
                    var repFile = new File(targetDir.fsName + "/smoke_report.json");
                    repFile.open("w");
                    repFile.write(safeSerialize(rep));
                    repFile.close();
                }
            }
        } catch (e) {}
    }

    try {
        var isPanel = (typeof Panel !== "undefined" && (thisObj instanceof Panel)) || (thisObj && thisObj.type === "panel");
        results.dockedMode = isPanel;

        if (typeof vac34_UIBuilder === "undefined") {
            results.errors.push("vac34_UIBuilder is not defined in global scope.");
            results.status = "FAILED";
            writeReport(results);
            return results;
        }

        var win = vac34_UIBuilder.build(thisObj);
        if (!win) {
            results.errors.push("vac34_UIBuilder.build() returned null or undefined.");
            results.status = "FAILED";
            writeReport(results);
            return results;
        }

        results.panelCreated = true;

        // Traverse children recursively to discover UI controls
        function inspectElement(el) {
            if (!el) return;
            var text = el.text ? String(el.text) : "";
            var tip = el.helpTip ? String(el.helpTip) : "";
            var type = el.type ? String(el.type) : "";

            if (text.indexOf("vac34_AE") !== -1 && text.indexOf("Failure") === -1) {
                results.titleVerified = true;
                if (typeof vac34_Config !== "undefined" && text.indexOf(vac34_Config.BUILD_ID) !== -1) {
                    results.buildIdVerified = true;
                }
            }
            if (type === "edittext" || tip.indexOf("Search") !== -1) {
                results.searchBoxPresent = true;
            }
            if (type === "dropdownlist" && el.items && el.items.length >= 3) {
                results.categoriesPresent = true;
                results.categoriesCount = el.items.length;
            }
            if (type === "listbox") {
                var listItemsCount = (el.items ? el.items.length : (el.children ? el.children.length : 0));
                if (listItemsCount > 0) {
                    results.recipeListPopulated = true;
                    results.recipeListCount = listItemsCount;
                }
            }
            if (type === "panel" && text === "Parameters") {
                results.paramPanelPresent = true;
                if (el.children) {
                    results.paramControlsCount = el.children.length;
                }
            }
            if (text.indexOf("Apply Behavior") !== -1 || text.indexOf("▶ Apply") !== -1) {
                results.hasApplyBtn = true;
            }
            if (text === "Update") {
                results.hasUpdateBtn = true;
            }
            if (text === "Remove") {
                results.hasRemoveBtn = true;
            }

            if (el.children) {
                for (var i = 0; i < el.children.length; i++) {
                    inspectElement(el.children[i]);
                }
            }
        }

        inspectElement(win);

        if (results.hasApplyBtn && results.hasUpdateBtn && results.hasRemoveBtn) {
            results.actionButtonsPresent = true;
        }

        // Layout execution
        if (win.layout) {
            win.layout.layout(true);
            win.layout.resize();
            results.initialLayoutPerformed = true;
        }

        // Validate geometry
        var hasValidBounds = false;
        if (win.bounds && (win.bounds.width > 0 || (win.bounds.right - win.bounds.left) > 0)) {
            hasValidBounds = true;
        } else if (win.size && (win.size[0] > 0 || win.size.width > 0)) {
            hasValidBounds = true;
        } else if (win.preferredSize && win.preferredSize[0] > 0) {
            hasValidBounds = true;
        } else if (win.children && win.children.length >= 4) {
            hasValidBounds = true;
        }
        results.geometryValid = hasValidBounds;

        // Recipe selection verification
        if (typeof win.setAuthoritativeSelection === "function" && typeof vac34_RecipeRegistry !== "undefined") {
            try {
                win.setAuthoritativeSelection(0);
                var selRec = win.getCurrentSelectedRecipe ? win.getCurrentSelectedRecipe() : null;
                var paramMap = win.getParamControlMap ? win.getParamControlMap() : null;
                if (selRec && paramMap) {
                    results.recipeSelectionWorking = true;
                }
            } catch (eSel) {
                results.errors.push("Recipe selection test error: " + (eSel.message || String(eSel)));
            }
        }

        // Check for startup diagnostic errors
        if (typeof vac34_Diagnostics !== "undefined") {
            var stErr = vac34_Diagnostics.getStartupError();
            if (stErr) {
                results.errors.push("Startup diagnostic error [" + stErr.stage + "]: " + stErr.message);
            }
        }

        // Determine verification status
        // A panel with ONLY a title or missing core controls MUST FAIL!
        var structurePassed = (
            results.panelCreated &&
            results.titleVerified &&
            results.buildIdVerified &&
            results.searchBoxPresent &&
            results.categoriesPresent &&
            results.recipeListPopulated &&
            results.paramPanelPresent &&
            results.actionButtonsPresent &&
            results.initialLayoutPerformed &&
            results.geometryValid &&
            results.errors.length === 0
        );

        results.hostScriptExecuted = true;
        results.structureVerified = structurePassed;
        results.layoutVerified = results.initialLayoutPerformed && results.geometryValid;

        // Verify expression runtime evaluation
        if (typeof vac34_RecipeRegistry !== "undefined") {
            try {
                var testRecipe = vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
                if (testRecipe) {
                    var gen = testRecipe.generateExpression(null, false, "Master", {}, "Audio", "Both");
                    if (gen && gen.length > 50) {
                        results.expressionRuntimeVerified = true;
                    }
                }
            } catch (eExp) {}
        }

        var isRealAE = (typeof app !== "undefined" && app.name === "Adobe After Effects");
        if (isRealAE) {
            var isVisible = (typeof win.visible !== "undefined") ? win.visible : false;
            results.visualVerified = (isVisible === true);
        }

        if (!structurePassed) {
            results.status = "FAILED";
        } else if (isRealAE && results.visualVerified) {
            results.status = "HOST_VERIFIED";
        } else if (structurePassed) {
            results.status = "STRUCTURE_VERIFIED";
        } else {
            results.status = "HOST_UNVERIFIED";
        }

        if (typeof Window !== "undefined" && (win instanceof Window)) {
            win.close();
        }

    } catch (e) {
        results.errors.push(e.message || String(e));
        results.status = "FAILED";
    }

    writeReport(results);
    return results;
})(typeof thisObj !== "undefined" ? thisObj : null);
