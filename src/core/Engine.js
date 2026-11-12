/*
 * vac34_AE — Master Expressions Studio
 * Engine: Execution Orchestrator with Rigorous Dependency Validation & Reversible Transactions
 */

var vac34_Engine = (function() {
    function findVac34PropertyOnLayer(layer, recipeId) {
        if (!layer) return null;
        // Check transform properties
        var xform = layer.property("Transform");
        if (xform) {
            for (var p = 1; p <= xform.numProperties; p++) {
                var prop = xform.property(p);
                if (prop && vac34_AEDom.isVac34Expression(prop)) {
                    if (!recipeId || vac34_AEDom.extractVac34RecipeId(prop) === recipeId) {
                        return prop;
                    }
                }
            }
        }
        return null;
    }

    // Classify the resolved property against the recipe's declared targets.
    // targetProperties: ["Any.Property"] = universal accept; a dotted
    // requirement matches the full path in either separator style AE and the
    // path printer use. A mismatch is reported to the caller as a warning
    // instead of silently blocking: the hard safety gate is dimension/type
    // compatibility, and effect properties legitimately carry this recipe.
    // ponytail: declared-target enforcement stops here; harden when the
    // registry starts declaring effect-scoped targets.
    function targetPropertiesAllowed(recipe, targetItem) {
        if (!recipe || !recipe.targetProperties) return true;
        var reqs = recipe.targetProperties;
        if (!reqs || reqs.length === 0) return true;
        if (reqs.indexOf("Any.Property") !== -1) return true;
        var prop = targetItem.prop;
        var propName = prop && (prop.name || "");
        var rawPath = (targetItem && targetItem.path) || "";
        var inspPath = (targetItem.inspected && targetItem.inspected.path) || "";
        var paths = [rawPath, inspPath];
        for (var r = 0; r < reqs.length; r++) {
            if (propName === reqs[r]) return true;
        }
        for (var pi = 0; pi < paths.length; pi++) {
            var p = paths[pi];
            if (!p) continue;
            p = p.replace(/\s*>\s*/g, ".");
            for (var ri = 0; ri < reqs.length; ri++) {
                var req = reqs[ri];
                if (p === req) return true;
                if (p.length > req.length && p.indexOf(req) !== -1) return true;
            }
        }
        return false;
    }

    return {
        applyRecipe: function(comp, layers, recipe, paramValues, isMasterMode, audioName, audioChan, targetMode) {
            try {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!layers) layers = vac34_AEDom.getSelectedLayers(comp);
            if (!recipe) return { ok: false, status: "NO_RECIPE", message: "No behavior recipe selected." };

            // P0: Audio Source Validation
            if (recipe.requiresAudio) {
                var audioVal = vac34_AudioEngine.validateAudioSource(comp, audioName, audioChan);
                if (!audioVal.valid) {
                    return {
                        ok: false,
                        status: (audioVal.state === "CHANNEL_MISSING") ? "CHANNEL_MISSING" : "AUDIO_MISSING",
                        appliedCount: 0,
                        failedCount: 0,
                        conflictCount: 0,
                        skipCount: 0,
                        message: audioVal.message,
                        warnings: []
                    };
                }
            }

            // P0: Universal Target Resolution.
            // PINNED mode resolves the structurately pinned property itself; a
            // missing or ambiguous pin fails closed instead of silently
            // retargeting whatever the viewer happens to have selected.
            var targetRes = null;
            if (targetMode === "PINNED") {
                var pinRes = vac34_AEDom.resolvePinnedTarget();
                if (!pinRes.ok) {
                    var pinStatus = "TARGET_MISSING";
                    if (pinRes.error === "PINNED_TARGET_REACQUIRE_FAILED" || pinRes.error === "PINNED_TARGET_MISMATCH" || pinRes.error === "PINNED_LAYER_AMBIGUOUS") {
                        pinStatus = "TARGET_REACQUIRE_FAILED";
                    } else if (pinRes.error === "PINNED_LAYER_MISSING" || pinRes.error === "PINNED_COMP_MISSING") {
                        pinStatus = "TARGET_MISSING";
                    }
                    return {
                        ok: false,
                        status: pinStatus,
                        appliedCount: 0,
                        failedCount: 0,
                        conflictCount: 0,
                        skipCount: 0,
                        message: pinRes.message,
                        warnings: []
                    };
                }
                // The mandatory compatibility gate applies to every target mode.
                // PINNED only changes how the property is found, never which
                // safety rules run.
                var insp = (typeof vac34_TargetResolver !== "undefined" && vac34_TargetResolver.inspectProperty)
                    ? vac34_TargetResolver.inspectProperty(pinRes.layer, pinRes.prop)
                    : null;
                var compatCheck = (insp && typeof vac34_TargetResolver.checkPropertyCompatibility === "function")
                    ? vac34_TargetResolver.checkPropertyCompatibility(insp, recipe)
                    : { compatible: false, reason: "TargetResolver unavailable; compatibility cannot be verified." };
                if (!compatCheck.compatible) {
                    return {
                        ok: false,
                        status: "TARGET_INCOMPATIBLE",
                        appliedCount: 0,
                        failedCount: 0,
                        conflictCount: 0,
                        skipCount: 1,
                        message: compatCheck.reason,
                        warnings: []
                    };
                }
                targetRes = {
                    ok: true,
                    targets: [{
                        layer: pinRes.layer,
                        prop: pinRes.prop,
                        descriptor: vac34_AEDom.capturePropertyDescriptor(pinRes.layer, pinRes.prop),
                        inspected: insp,
                        path: pinRes.path
                    }],
                    incompatibleCount: 0,
                    message: "Pinned target resolved."
                };
            } else {
                targetRes = (typeof vac34_TargetResolver !== "undefined")
                    ? vac34_TargetResolver.resolveTargets(comp, layers, recipe, targetMode)
                    : { ok: false, targets: [], message: "TargetResolver not available." };
            }

            if (targetRes && targetRes.targets && targetRes.targets.length > 0 &&
                typeof vac34_TargetResolver !== "undefined" && vac34_TargetResolver.inspectProperty) {
                for (var ins = 0; ins < targetRes.targets.length; ins++) {
                    if (!targetRes.targets[ins].inspected) {
                        targetRes.targets[ins].inspected = vac34_TargetResolver.inspectProperty(targetRes.targets[ins].layer, targetRes.targets[ins].prop);
                    }
                }
            }

            // One mandatory compatibility gate for every target mode. A mode
            // decides only how a property is discovered, never which safety
            // rules run, so RECIPE_DEFAULT / AUTO fallbacks cannot bypass the
            // checks PINNED already ran.
            if (targetRes && targetRes.targets && targetRes.targets.length > 0) {
                var gateFail = (targetRes.incompatibleCount || 0) > 0;
                for (var gt = 0; gt < targetRes.targets.length; gt++) {
                    var gTarget = targetRes.targets[gt];
                    var gInsp = gTarget.inspected ||
                        ((typeof vac34_TargetResolver !== "undefined" && vac34_TargetResolver.inspectProperty)
                            ? vac34_TargetResolver.inspectProperty(gTarget.layer, gTarget.prop)
                            : null);
                    var gCheck = (gInsp && typeof vac34_TargetResolver !== "undefined" && vac34_TargetResolver.checkPropertyCompatibility)
                        ? vac34_TargetResolver.checkPropertyCompatibility(gInsp, recipe)
                        : { compatible: false, reason: "TargetResolver unavailable; compatibility cannot be verified." };
                    if (!gCheck.compatible) {
                        targetRes.incompatibleCount = (targetRes.incompatibleCount || 0) + 1;
                        targetRes.targets.splice(gt, 1);
                        gt--;
                        continue;
                    }
                    if (!targetPropertiesAllowed(recipe, gTarget)) {
                        gTarget._targetPropertyMismatch = recipe.targetProperties.join(", ");
                    }
                    gTarget.inspected = gInsp;
                }
            }

            if (!targetRes.ok || targetRes.targets.length === 0) {
                var incompatible = targetRes.incompatibleCount || 0;
                return {
                    ok: false,
                    status: (incompatible > 0) ? "TARGET_INCOMPATIBLE" : "TARGET_MISSING",
                    appliedCount: 0,
                    failedCount: 0,
                    conflictCount: 0,
                    skipCount: incompatible,
                    message: targetRes.message,
                    warnings: []
                };
            }

            // Filter out foreign expressions and different vac34 recipes to prevent silent overwrites
            var validTargets = [];
            var foreignConflicts = [];
            var recipeConflicts = [];
            for (var t = 0; t < targetRes.targets.length; t++) {
                var item = targetRes.targets[t];
                var classRes = vac34_AEDom.classifyExpression(item.prop, recipe.id);
                if (classRes.state === "FOREIGN") {
                    foreignConflicts.push(item);
                } else if (classRes.state === "DIFFERENT_RECIPE") {
                    item._conflictRecipeId = classRes.recipeId;
                    recipeConflicts.push(item);
                } else {
                    validTargets.push(item);
                }
            }

            if (recipeConflicts.length > 0 && validTargets.length === 0) {
                return {
                    ok: false,
                    status: "EXPRESSION_CONFLICT",
                    appliedCount: 0,
                    failedCount: 0,
                    conflictCount: recipeConflicts.length,
                    skipCount: 0,
                    message: "Cannot apply: property already has active recipe '" + recipeConflicts[0]._conflictRecipeId + "'. Silent overwrite is prevented.",
                    warnings: ["Prevented overwrite of active recipe '" + recipeConflicts[0]._conflictRecipeId + "' on " + recipeConflicts[0].path]
                };
            }

            if (foreignConflicts.length > 0 && validTargets.length === 0) {
                return {
                    ok: false,
                    status: "EXPRESSION_CONFLICT",
                    appliedCount: 0,
                    failedCount: 0,
                    conflictCount: foreignConflicts.length,
                    skipCount: 0,
                    message: "Cannot apply: selected property has foreign expression which must not be overwritten.",
                    warnings: ["Preserved foreign expression on " + foreignConflicts[0].path]
                };
            }

            vac34_AEDom.beginUndo("vac34_AE: Apply " + recipe.displayName);
            var successCount = 0;
            var failureCount = 0;
            var warnings = [];
            var lastAppliedPath = "";
            var lastFailurePath = "";

            try {
                var masterLayer = null;
                var masterControls = null;
                var masterIsNew = false;
                if (isMasterMode) {
                    masterLayer = vac34_ControllerManager.getOrCreateMasterLayer(comp);
                    if (!masterLayer) {
                        return { ok: false, status: "CONTROLLER_SETUP_FAILED", appliedCount: 0, failedCount: validTargets.length, message: "Failed to create Shared Master Null." };
                    }
                    masterIsNew = !!masterLayer._vac34IsNew;
                    masterControls = vac34_ControllerManager.setupRecipeControls(masterLayer, recipe, paramValues);
                    if (!masterControls) {
                        if (masterIsNew) {
                            try { masterLayer.remove(); } catch (e) {}
                        }
                        return { ok: false, status: "CONTROLLER_SETUP_FAILED", appliedCount: 0, failedCount: validTargets.length, message: "Failed to initialize Expression Controls on Master Null." };
                    }
                }

                for (var v = 0; v < validTargets.length; v++) {
                    var targetItem = validTargets[v];
                    var lyr = targetItem.layer;
                    var prop = targetItem.prop;
                    var ctrlMap = null;

                    // Capture survival descriptor before any structural DOM mutation
                    if (!targetItem.descriptor && vac34_AEDom.capturePropertyDescriptor) {
                        targetItem.descriptor = vac34_AEDom.capturePropertyDescriptor(lyr, prop);
                    }

                    if (!isMasterMode) {
                        ctrlMap = vac34_ControllerManager.setupRecipeControls(lyr, recipe, paramValues);
                        if (!ctrlMap) {
                            failureCount++;
                            lastFailurePath = targetItem.path;
                            warnings.push("CONTROLLER_SETUP_FAILED on layer '" + lyr.name + "'.");
                            continue;
                        }

                        // P0: Property Reference Survival Strategy
                        // Reacquire fresh target reference because adding Controls can invalidate previous references.
                        // A stale reference must never be written to: fail closed instead.
                        if (!targetItem.descriptor || !vac34_AEDom.reacquireProperty) {
                            if (ctrlMap && ctrlMap._tx) { ctrlMap._tx.rollback(); }
                            failureCount++;
                            lastFailurePath = targetItem.path;
                            warnings.push("TARGET_REACQUIRE_FAILED on " + targetItem.path + ": property descriptor missing after controller setup.");
                            continue;
                        }
                        var reacquired = vac34_AEDom.reacquireProperty(lyr, targetItem.descriptor);
                        if (!reacquired) {
                            if (ctrlMap && ctrlMap._tx) { ctrlMap._tx.rollback(); }
                            failureCount++;
                            lastFailurePath = targetItem.path;
                            warnings.push("TARGET_REACQUIRE_FAILED on " + targetItem.path + ": property instance could not be uniquely restored.");
                            continue;
                        }
                        prop = reacquired;
                        // Validate reacquired property matches original by name and matchName
                        if (prop.name !== targetItem.prop.name || prop.matchName !== targetItem.prop.matchName) {
                            if (ctrlMap && ctrlMap._tx) { ctrlMap._tx.rollback(); }
                            failureCount++;
                            lastFailurePath = targetItem.path;
                            warnings.push("TARGET_REACQUIRE_MISMATCH on " + targetItem.path + ": reacquired property '" + prop.name + "' differs from original '" + targetItem.prop.name + "'.");
                            continue;
                        }
                    }

                    var masterName = masterLayer ? masterLayer.name : vac34_Config.MASTER_LAYER_NAME;

                    // P0: snapshot pre-assignment expression state so a failed apply restores it byte-for-byte
                    var prevExprText = "";
                    var hadPrevExpr = false;
                    var prevEnabled = undefined;
                    try { prevExprText = prop.expression || ""; } catch (ePrev) { prevExprText = ""; }
                    hadPrevExpr = (prevExprText.replace(/^\s+|\s+$/g, "") !== "");
                    try { prevEnabled = prop.expressionEnabled; } catch (eEn) { prevEnabled = undefined; }

                    try {
                        var expr = recipe.generateExpression(lyr, isMasterMode, masterName, paramValues, audioName, audioChan);
                        prop.expression = expr;

                        // P1: Validate expression evaluation state immediately
                        var exprState = vac34_AEDom.verifyExpressionState(prop);
                        if (!exprState.ok) {
                            throw new Error(exprState.error);
                        }

                        if (ctrlMap && ctrlMap._tx) {
                            ctrlMap._tx.commit();
                        }
                        successCount++;
                        lastAppliedPath = targetItem.path;
                    } catch (exprErr) {
                        // P0: restore the exact previous expression before touching anything else
                        var restoreOk = true;
                        try {
                            prop.expression = prevExprText;
                            if (prevEnabled !== undefined) {
                                try { prop.expressionEnabled = prevEnabled; } catch (eRestoreEnabled) {}
                            }
                            if ((prop.expression || "") !== prevExprText) {
                                restoreOk = false;
                            }
                        } catch (eRestore) {
                            restoreOk = false;
                        }

                        if (ctrlMap && ctrlMap._tx) {
                            ctrlMap._tx.rollback();
                            if (ctrlMap._tx.failedOperations.length > 0) {
                                restoreOk = false;
                            }
                        }
                        failureCount++;
                        lastFailurePath = targetItem.path;
                        warnings.push((restoreOk ? "EXPRESSION_ERROR on " : "ROLLBACK_INCOMPLETE on ") + targetItem.path + ": " + exprErr.message);
                    }
                }

                if (isMasterMode && masterControls && masterControls._tx) {
                    if (successCount === 0) {
                        masterControls._tx.rollback();
                        if (masterIsNew && masterLayer) {
                            try { masterLayer.remove(); } catch (eM) {}
                        }
                    } else {
                        masterControls._tx.commit();
                    }
                }
            } finally {
                vac34_AEDom.endUndo();
            }

            var successMsg = "";
            if (successCount === 1) {
                successMsg = "Applied " + recipe.displayName + " to " + lastAppliedPath;
            } else if (successCount > 1) {
                successMsg = "Applied " + recipe.displayName + " to " + successCount + " properties.";
            } else {
                successMsg = "Failed to apply " + recipe.displayName + "." + (lastFailurePath ? (" Affected: " + lastFailurePath) : "");
            }

            // A batch with any failed, skipped or conflicted target is never
            // reported as fully verified: one successful property cannot
            // launder the outcome of the rest of the batch.
            var skippedCount = targetRes.incompatibleCount || 0;
            var conflictTotal = foreignConflicts.length + recipeConflicts.length;
            var applyStatus;
            if (successCount === 0) {
                var rollbackIncomplete = false;
                for (var w = 0; w < warnings.length; w++) {
                    if (warnings[w].indexOf("ROLLBACK_INCOMPLETE") === 0) {
                        rollbackIncomplete = true;
                    }
                }
                applyStatus = rollbackIncomplete ? "APPLY_FAILED_ROLLBACK_INCOMPLETE" : "APPLY_FAILED_ROLLED_BACK";
            } else if (failureCount === 0 && skippedCount === 0 && conflictTotal === 0) {
                applyStatus = "APPLIED_VERIFIED";
            } else {
                applyStatus = "PARTIAL_SUCCESS";
                var parts = [];
                parts.push(successCount + " applied");
                if (failureCount > 0) parts.push(failureCount + " failed");
                if (skippedCount > 0) parts.push(skippedCount + " incompatible");
                if (conflictTotal > 0) parts.push(conflictTotal + " conflicted");
                successMsg += " (" + parts.join(", ") + ")";
            }

            return {
                ok: (successCount > 0),
                status: applyStatus,
                appliedCount: successCount,
                failedCount: failureCount,
                conflictCount: conflictTotal,
                skipCount: skippedCount,
                message: successMsg,
                warnings: warnings
            };
            } catch (unexpectedErr) {
                return {
                    ok: false,
                    status: "UNEXPECTED_ERROR",
                    appliedCount: 0,
                    failedCount: 0,
                    conflictCount: 0,
                    skipCount: 0,
                    message: "Unexpected error during Apply: " + (unexpectedErr && (unexpectedErr.message || unexpectedErr.toString())),
                    warnings: []
                };
            }
        },

        updateParameters: function(comp, layers, recipe, paramValues, isMasterMode, targetMode) {
            try {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!layers) layers = vac34_AEDom.getSelectedLayers(comp);
            if (!recipe || !paramValues) return { ok: false, status: "NO_RECIPE", updatedCount: 0, message: "Missing recipe or parameters." };

            vac34_AEDom.beginUndo("vac34_AE: Update " + recipe.displayName);
            var updatedCount = 0;

            try {
                if (targetMode === "PINNED") {
                    var pinRes = vac34_AEDom.resolvePinnedTarget();
                    if (!pinRes.ok) {
                        return {
                            ok: false,
                            status: (pinRes.error === "TARGET_NOT_PINNED") ? "TARGET_NOT_PINNED" : "TARGET_REACQUIRE_FAILED",
                            updatedCount: 0,
                            message: pinRes.message || pinRes.error
                        };
                    }
                    // Target identity (what is animated) and controller ownership
                    // (where the parameters physically live) are independent:
                    // PINNED selects the former, the controller mode decides the
                    // latter. A master-mode update must hit the master null's
                    // controls, never the pinned target layer's.
                    var pinOwnerLayer = pinRes.layer;
                    if (isMasterMode) {
                        var pinnedOwnerMaster = vac34_ControllerManager.findMasterLayer(comp);
                        if (!pinnedOwnerMaster) {
                            return {
                                ok: false,
                                status: "CONTROLLER_MISSING",
                                updatedCount: 0,
                                message: "Shared Master Null not found; no master controls to update."
                            };
                        }
                        pinOwnerLayer = pinnedOwnerMaster;
                    }
                    for (var pId in paramValues) {
                        if (paramValues.hasOwnProperty(pId)) {
                            if (vac34_ControllerManager.updateParameterValue(pinOwnerLayer, recipe, pId, paramValues[pId])) {
                                updatedCount++;
                            }
                        }
                    }
                } else if (isMasterMode) {
                    // Find-only: an Update never creates a master null.
                    var master = vac34_ControllerManager.findMasterLayer(comp);
                    if (master) {
                        for (var pId in paramValues) {
                            if (paramValues.hasOwnProperty(pId)) {
                                if (vac34_ControllerManager.updateParameterValue(master, recipe, pId, paramValues[pId])) {
                                    updatedCount++;
                                }
                            }
                        }
                    } else {
                        return {
                            ok: false,
                            status: "CONTROLLER_MISSING",
                            updatedCount: 0,
                            message: "Shared Master Null not found; no master controls to update."
                        };
                    }
                } else {
                    for (var i = 0; i < layers.length; i++) {
                        var lyr = layers[i];
                        for (var pId in paramValues) {
                            if (paramValues.hasOwnProperty(pId)) {
                                if (vac34_ControllerManager.updateParameterValue(lyr, recipe, pId, paramValues[pId])) {
                                    updatedCount++;
                                }
                            }
                        }
                    }
                }
            } finally {
                vac34_AEDom.endUndo();
            }

            var ok = (updatedCount > 0);
            return {
                ok: ok,
                status: ok ? "UPDATED" : "NOTHING_TO_UPDATE",
                updatedCount: updatedCount,
                message: ok ? "Successfully updated " + updatedCount + " parameter value(s)." : "No matching active controls found to update."
            };
            } catch (unexpectedErr) {
                return {
                    ok: false,
                    status: "UNEXPECTED_ERROR",
                    updatedCount: 0,
                    message: "Unexpected error during Update: " + (unexpectedErr && (unexpectedErr.message || unexpectedErr.toString()))
                };
            }
        },

        removeRecipe: function(comp, layers, recipe, scope, targetMode) {
            try {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!layers) layers = vac34_AEDom.getSelectedLayers(comp);
            if (!recipe) return { ok: false, status: "NO_RECIPE", removedCount: 0, message: "No recipe selected." };

            var actualScope = scope;
            if (!actualScope) {
                if (targetMode === "PINNED") {
                    actualScope = "PINNED";
                } else if (targetMode === "SELECTED_PROPERTY" || (typeof vac34_TargetResolver !== "undefined" && vac34_TargetResolver.getTargetMode() === "SELECTED_PROPERTY")) {
                    actualScope = "SELECTED_PROPERTY";
                } else {
                    var selProps = (typeof vac34_TargetResolver !== "undefined") ? vac34_TargetResolver.getSelectedProperties(comp) : [];
                    actualScope = (selProps.length > 0) ? "SELECTED_PROPERTY" : "SELECTED_LAYERS";
                }
            }

            vac34_AEDom.beginUndo("vac34_AE: Remove " + recipe.displayName);
            var removedCount = 0;
            var controlsRemoved = 0;

            try {
                if (actualScope === "PINNED") {
                    var pinRes = vac34_AEDom.resolvePinnedTarget();
                    if (!pinRes.ok) {
                        return {
                            ok: false,
                            status: (pinRes.error === "TARGET_NOT_PINNED") ? "TARGET_NOT_PINNED" : "TARGET_REACQUIRE_FAILED",
                            removedCount: 0,
                            scope: actualScope,
                            message: pinRes.message || pinRes.error
                        };
                    }
                    if (vac34_AEDom.isVac34Expression(pinRes.prop) && vac34_AEDom.extractVac34RecipeId(pinRes.prop) === recipe.id) {
                        pinRes.prop.expression = "";
                        removedCount++;

                        // Controller lifecycle with reference counting: per-layer
                        // controls die with the last consumer on their layer;
                        // shared master controls survive while any layer in the
                        // comp still consumes this recipe. Ownership checks inside
                        // removeRecipeControls keep foreign effects untouched.
                        try {
                            var remainingOnLayer = vac34_AEDom.findRecipeProperties(pinRes.layer, recipe.id).length;
                            if (remainingOnLayer === 0) {
                                controlsRemoved += vac34_ControllerManager.removeRecipeControls(pinRes.layer, recipe);
                            }
                            var masterRig = vac34_ControllerManager.findMasterLayer(comp);
                            if (masterRig) {
                                var compConsumers = 0;
                                if (comp && comp.numLayers) {
                                    for (var mc = 1; mc <= comp.numLayers; mc++) {
                                        var mcLyr = comp.layer(mc);
                                        if (mcLyr) {
                                            compConsumers += vac34_AEDom.findRecipeProperties(mcLyr, recipe.id).length;
                                        }
                                    }
                                }
                                if (compConsumers === 0) {
                                    controlsRemoved += vac34_ControllerManager.removeRecipeControls(masterRig, recipe);
                                }
                            }
                        } catch (eCtrl) {}
                    }
                } else if (actualScope === "SELECTED_PROPERTY") {
                    var targets = (typeof vac34_TargetResolver !== "undefined")
                        ? vac34_TargetResolver.getSelectedProperties(comp)
                        : [];

                    for (var t = 0; t < targets.length; t++) {
                        var p = targets[t];
                        if (vac34_AEDom.isVac34Expression(p) && vac34_AEDom.extractVac34RecipeId(p) === recipe.id) {
                            try {
                                p.expression = "";
                                removedCount++;
                            } catch (eExp) {}
                        }
                    }

                    // Check if remaining properties on layers still use this recipe before removing controls
                    if (layers && layers.length > 0) {
                        for (var l = 0; l < layers.length; l++) {
                            var chkLyr = layers[l];
                            var remaining = vac34_AEDom.findRecipeProperties(chkLyr, recipe.id);
                            if (remaining.length === 0) {
                                vac34_ControllerManager.removeRecipeControls(chkLyr, recipe);
                            }
                        }
                    }
                } else if (actualScope === "ALL_IN_COMP") {
                    if (comp && comp.numLayers) {
                        for (var c = 1; c <= comp.numLayers; c++) {
                            var cLyr = comp.layer(c);
                            var cProps = vac34_AEDom.findRecipeProperties(cLyr, recipe.id);
                            for (var cp = 0; cp < cProps.length; cp++) {
                                try {
                                    cProps[cp].expression = "";
                                    removedCount++;
                                } catch (eC) {}
                            }
                            if (cProps.length > 0) {
                                vac34_ControllerManager.removeRecipeControls(cLyr, recipe);
                            }
                        }
                    }
                } else {
                    // SELECTED_LAYERS scope
                    for (var i = 0; i < layers.length; i++) {
                        var lyr = layers[i];
                        var ownedProps = (typeof vac34_AEDom.findRecipeProperties === "function")
                            ? vac34_AEDom.findRecipeProperties(lyr, recipe.id)
                            : [];

                        if (ownedProps.length === 0) {
                            var fallbackProp = vac34_AEDom.findRecipeProperty(lyr, recipe.id);
                            if (fallbackProp) ownedProps.push(fallbackProp);
                        }

                        if (ownedProps.length > 0) {
                            for (var pIdx = 0; pIdx < ownedProps.length; pIdx++) {
                                try {
                                    ownedProps[pIdx].expression = "";
                                    removedCount++;
                                } catch (eExp2) {}
                            }
                            vac34_ControllerManager.removeRecipeControls(lyr, recipe);
                        }
                    }
                }
            } finally {
                vac34_AEDom.endUndo();
            }

            return {
                ok: (removedCount > 0),
                status: (removedCount > 0) ? "REMOVED" : "NOTHING_TO_REMOVE",
                removedCount: removedCount,
                controlsRemoved: controlsRemoved,
                scope: actualScope,
                message: (removedCount > 0)
                    ? ("Removed '" + recipe.displayName + "' from " + removedCount + " property(ies)" +
                       (controlsRemoved > 0 ? ("; cleaned " + controlsRemoved + " unreferenced controller(s).") : "; no orphan controllers removed (shared or still referenced)."))
                    : ("No active '" + recipe.displayName + "' expressions found to remove.")
            };
            } catch (unexpectedErr) {
                return {
                    ok: false,
                    status: "UNEXPECTED_ERROR",
                    removedCount: 0,
                    message: "Unexpected error during Remove: " + (unexpectedErr && (unexpectedErr.message || unexpectedErr.toString()))
                };
            }
        }
    };
})();
