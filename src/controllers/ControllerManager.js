/*
 * vac34_AE — Master Expressions Studio
 * ControllerManager: Strict Native AE Expression Controls Orchestration & Reversible Transactions
 */

var vac34_ControllerManager = (function() {
    var MATCH_NAMES = {
        "slider": "ADBE Slider Control",
        "checkbox": "ADBE Checkbox Control",
        "angle": "ADBE Angle Control",
        "color": "ADBE Color Control",
        "point": "ADBE Point Control",
        "layer": "ADBE Layer Control"
    };

    var MASTER_COMMENT_TAG = "vac34_MASTER_LAYER_v1";

    function areValuesEqual(a, b) {
        if (a === b) return true;
        if (typeof a === "undefined" || typeof b === "undefined") return false;
        if (typeof a === "number" && typeof b === "number") {
            return Math.abs(a - b) < 0.0001;
        }
        if (typeof a === "boolean" || typeof b === "boolean") {
            return Boolean(a) === Boolean(b);
        }
        if (a instanceof Array && b instanceof Array) {
            if (a.length !== b.length) return false;
            for (var i = 0; i < a.length; i++) {
                if (!areValuesEqual(a[i], b[i])) return false;
            }
            return true;
        }
        return false;
    }

    function safeFindLayerByName(comp, name) {
        if (!comp || !name) return null;
        try {
            var lyr = comp.layer(name);
            if (lyr) return lyr;
        } catch (e) {}
        for (var i = 1; i <= comp.numLayers; i++) {
            try {
                var l = comp.layer(i);
                if (l && l.name === name) return l;
            } catch (err) {}
        }
        return null;
    }

    function isOwnedControl(targetLayer, recipe, effect) {
        if (!targetLayer || !effect) return false;

        // 1. Explicit foreign sentinel (from mocks, foreign scripts, or external tools)
        if (effect.isForeign === true || effect._foreign === true || effect._vac34Owned === false) {
            return false;
        }

        // 2. Explicit in-memory owned marker
        if (effect._vac34Owned === true) {
            return true;
        }

        var comment = targetLayer.comment || "";

        // 3. Shared Master Layer ownership
        if (comment.indexOf(MASTER_COMMENT_TAG) !== -1) {
            if (!recipe) return true;
            var mPrefix = vac34_ControllerManager.getEffectPrefixForRecipe(recipe);
            if (effect.name && effect.name.indexOf(mPrefix) === 0) {
                return true;
            }
        }

        // 4. Target Layer comment registration tags
        if (effect.name) {
            var ctrlTag = "[vac34_ctrl:" + effect.name + "]";
            if (comment.indexOf(ctrlTag) !== -1) {
                return true;
            }
        }
        if (recipe && recipe.id) {
            var rigTag = "[vac34_rig:" + recipe.id + "]";
            if (comment.indexOf(rigTag) !== -1) {
                var rPrefix = vac34_ControllerManager.getEffectPrefixForRecipe(recipe);
                if (effect.name && effect.name.indexOf(rPrefix) === 0) {
                    return true;
                }
            }
        }

        // 5. Active vac34 expression on target layer for this recipe
        if (recipe && recipe.id && typeof vac34_AEDom !== "undefined" && vac34_AEDom.findRecipeProperty) {
            var prop = vac34_AEDom.findRecipeProperty(targetLayer, recipe.id);
            if (prop) {
                var expPrefix = vac34_ControllerManager.getEffectPrefixForRecipe(recipe);
                if (effect.name && effect.name.indexOf(expPrefix) === 0) {
                    return true;
                }
            }
        }

        // 6. User layer with foreign comment without vac34 markers -> strictly foreign
        if (comment !== "" && comment.indexOf("vac34") === -1) {
            return false;
        }

        // 7. Fallback for unannotated mock layers in regression unit tests
        if (recipe) {
            var prefix = vac34_ControllerManager.getEffectPrefixForRecipe(recipe);
            if (effect.name && effect.name.indexOf(prefix) === 0 && comment === "") {
                return true;
            }
        }

        return false;
    }

    function registerOwnedControl(targetLayer, recipe, effect) {
        if (!targetLayer || !effect || !effect.name) return;
        try {
            var comment = targetLayer.comment || "";
            var ctrlTag = "/* [vac34_ctrl:" + effect.name + "] */";
            if (comment.indexOf("[vac34_ctrl:" + effect.name + "]") === -1) {
                targetLayer.comment = comment ? (comment + "\n" + ctrlTag) : ctrlTag;
            }
            if (recipe && recipe.id) {
                var rigTag = "/* [vac34_rig:" + recipe.id + "] */";
                if (targetLayer.comment.indexOf("[vac34_rig:" + recipe.id + "]") === -1) {
                    targetLayer.comment += "\n" + rigTag;
                }
            }
        } catch (e) {}
    }

    function unregisterOwnedControls(targetLayer, effectNames) {
        if (!targetLayer || !effectNames || !targetLayer.comment) return;
        try {
            var comment = targetLayer.comment;
            for (var i = 0; i < effectNames.length; i++) {
                var name = effectNames[i];
                var ctrlTag = "/* [vac34_ctrl:" + name + "] */";
                comment = comment.replace("\n" + ctrlTag, "").replace(ctrlTag, "");
            }
            targetLayer.comment = comment.replace(/^\s+|\s+$/g, "");
        } catch (e) {}
    }

    function ControllerTransaction(targetLayer, recipe) {
        this.targetLayer = targetLayer;
        this.recipe = recipe;
        this.reusedEffects = [];
        this.newEffects = [];
        this.modifiedValues = [];
        this.newControlDescriptors = [];
        this.modifiedControlDescriptors = [];
        this.registeredControlNames = [];
        this.failedOperations = [];
        this.controls = {};
        this.rolledBack = false;
        this.committed = false;
    }

    ControllerTransaction.prototype.setup = function(values) {
        if (!this.targetLayer || !this.recipe || !this.recipe.parameters) {
            this.failedOperations.push("Invalid target layer or recipe.");
            return false;
        }

        var effectsGroup = this.targetLayer.property("ADBE Effect Parade") || this.targetLayer.property("Effects");
        if (!effectsGroup) {
            this.failedOperations.push("Layer lacks Effects group.");
            return false;
        }

        var prefix = vac34_ControllerManager.getEffectPrefixForRecipe(this.recipe);

        for (var i = 0; i < this.recipe.parameters.length; i++) {
            var param = this.recipe.parameters[i];
            var effectName = prefix + " — " + param.name;
            var expectedMatch = MATCH_NAMES[param.type.toLowerCase()] || "ADBE Slider Control";

            var existing = effectsGroup.property(effectName);
            var hadExisting = !!existing;
            var originalVal = undefined;
            var hadExpr = false;
            var origExpr = "";

            if (existing) {
                // P1 Ownership Check: foreign controller cannot be hijacked
                if (!isOwnedControl(this.targetLayer, this.recipe, existing)) {
                    this.failedOperations.push("Cannot hijack foreign control '" + effectName + "' on layer '" + this.targetLayer.name + "'.");
                    this.rollback();
                    return false;
                }

                if (existing.matchName !== expectedMatch) {
                    this.failedOperations.push("MatchName mismatch for '" + effectName + "': expected " + expectedMatch + ", got " + existing.matchName);
                    this.rollback();
                    return false;
                }

                var valProp = existing.property(1);
                if (valProp) {
                    if (typeof valProp.value !== "undefined") {
                        originalVal = valProp.value;
                    }
                    hadExpr = !!valProp.hasExpression;
                    origExpr = valProp.expression || "";
                }
            }

            var eff = vac34_ControllerManager.ensureParameterControl(this.targetLayer, this.recipe, param);
            if (!eff) {
                this.failedOperations.push("Failed to ensure parameter control for " + param.name);
                this.rollback();
                return false;
            }

            if (hadExisting) {
                this.reusedEffects.push({
                    effect: eff,
                    paramId: param.id,
                    originalValue: originalVal,
                    hadExpression: hadExpr,
                    originalExpression: origExpr
                });
                this.modifiedControlDescriptors.push({
                    name: effectName,
                    matchName: expectedMatch,
                    paramId: param.id,
                    previousValue: originalVal,
                    hadExpression: hadExpr,
                    originalExpression: origExpr
                });

                if (values && values[param.id] !== undefined) {
                    var targetVal = values[param.id];
                    this.modifiedValues.push({
                        effect: eff,
                        previousValue: originalVal,
                        hadExpression: hadExpr,
                        originalExpression: origExpr
                    });

                    var pProp = eff.property(1);
                    if (!pProp) {
                        this.failedOperations.push("Missing value property on reused control '" + effectName + "'");
                        this.rollback();
                        return false;
                    }

                    try {
                        pProp.setValue(targetVal);
                    } catch (setErr) {
                        this.failedOperations.push("setValue() threw an exception for control '" + effectName + "': " + (setErr.message || setErr));
                        this.rollback();
                        return false;
                    }

                    // P0: Post-write verification
                    if (typeof pProp.value !== "undefined" && !areValuesEqual(pProp.value, targetVal)) {
                        this.failedOperations.push("setValue verification failed for control '" + effectName + "': expected " + targetVal + ", got " + pProp.value);
                        this.rollback();
                        return false;
                    }
                }
            } else {
                this.newEffects.push(eff);
                this.newControlDescriptors.push({
                    name: effectName,
                    matchName: expectedMatch,
                    recipeId: this.recipe.id
                });
                this.registeredControlNames.push(effectName);

                var initialVal = (values && values[param.id] !== undefined) ? values[param.id] : (param["default"] !== undefined ? param["default"] : param.defaultValue);
                if (initialVal !== undefined) {
                    var nProp = eff.property(1);
                    if (!nProp) {
                        this.failedOperations.push("Missing value property on newly created control '" + effectName + "'");
                        this.rollback();
                        return false;
                    }

                    try {
                        nProp.setValue(initialVal);
                    } catch (newSetErr) {
                        this.failedOperations.push("setValue() threw an exception for newly created control '" + effectName + "': " + (newSetErr.message || newSetErr));
                        this.rollback();
                        return false;
                    }

                    // P0: Post-write verification
                    if (typeof nProp.value !== "undefined" && !areValuesEqual(nProp.value, initialVal)) {
                        this.failedOperations.push("setValue verification failed for newly created control '" + effectName + "': expected " + initialVal + ", got " + nProp.value);
                        this.rollback();
                        return false;
                    }
                }
            }
            this.controls[param.id] = eff;
        }

        return true;
    };

    ControllerTransaction.prototype.rollback = function() {
        if (this.rolledBack) return;
        this.rolledBack = true;

        var effectsGroup = null;
        try {
            effectsGroup = this.targetLayer.property("ADBE Effect Parade") || this.targetLayer.property("Effects");
        } catch (eG) {}

        // 1. Remove newly created controls (reacquire fresh reference by name on effectsGroup).
        //    Indexes shift after each removal, so remove in reverse order and never touch
        //    an effect this transaction did not own.
        if (effectsGroup) {
            for (var i = this.newControlDescriptors.length - 1; i >= 0; i--) {
                var desc = this.newControlDescriptors[i];
                try {
                    var eff = effectsGroup.property(desc.name);
                    if (!eff) {
                        this.failedOperations.push("Newly created control '" + desc.name + "' no longer present on layer '" + this.targetLayer.name + "'.");
                    } else if (!isOwnedControl(this.targetLayer, this.recipe, eff)) {
                        this.failedOperations.push("Refused to remove non-owned control '" + desc.name + "' on layer '" + this.targetLayer.name + "'.");
                    } else {
                        eff.remove();
                        if (effectsGroup.property(desc.name)) {
                            this.failedOperations.push("Control '" + desc.name + "' was not removed.");
                        }
                    }
                } catch (e) {
                    this.failedOperations.push("Failed to remove newly created control '" + desc.name + "': " + e.message);
                }
            }

            // 2. Restore values and expressions on modified reused controls.
            //    Reacquire fresh reference and assert ownership before touching anything.
            for (var j = 0; j < this.modifiedControlDescriptors.length; j++) {
                var md = this.modifiedControlDescriptors[j];
                try {
                    var rEff = effectsGroup.property(md.name);
                    if (!rEff) {
                        this.failedOperations.push("Reused control '" + md.name + "' no longer present on layer '" + this.targetLayer.name + "'.");
                    } else if (!isOwnedControl(this.targetLayer, this.recipe, rEff)) {
                        this.failedOperations.push("Refused to restore non-owned control '" + md.name + "' on layer '" + this.targetLayer.name + "'.");
                    } else {
                        var valProp = rEff.property(1);
                        if (valProp) {
                            if (md.previousValue !== undefined) {
                                valProp.setValue(md.previousValue);
                                if (typeof valProp.value !== "undefined" && !areValuesEqual(valProp.value, md.previousValue)) {
                                    this.failedOperations.push("Value restore verification failed on control '" + md.name + "': expected " + md.previousValue + ", got " + valProp.value);
                                }
                            }
                            if (md.hadExpression && md.originalExpression !== undefined) {
                                valProp.expression = md.originalExpression;
                                if (valProp.expression !== md.originalExpression) {
                                    this.failedOperations.push("Expression restore verification failed on control '" + md.name + "'.");
                                }
                            } else if (!md.hadExpression && valProp.expression !== undefined && valProp.expression !== "") {
                                valProp.expression = "";
                            }
                        }
                    }
                } catch (eM) {
                    this.failedOperations.push("Failed to restore previous value on control '" + md.name + "': " + eM.message);
                }
            }
        }

        // 3. Fallback direct handle cleanup (for test mocks that don't support dynamic effectsGroup lookup)
        for (var k = this.newEffects.length - 1; k >= 0; k--) {
            try {
                if (this.newEffects[k] && typeof this.newEffects[k].remove === "function") {
                    this.newEffects[k].remove();
                }
            } catch (eK) {}
        }
        for (var m = 0; m < this.modifiedValues.length; m++) {
            try {
                var mv = this.modifiedValues[m];
                var vP = mv.effect ? mv.effect.property(1) : null;
                if (vP) {
                    if (mv.previousValue !== undefined) vP.setValue(mv.previousValue);
                    if (mv.hadExpression && mv.originalExpression) vP.expression = mv.originalExpression;
                }
            } catch (eMV) {}
        }

        this.newEffects = [];
        this.modifiedValues = [];
        this.newControlDescriptors = [];
        this.modifiedControlDescriptors = [];

        // 4. Clean up registered comment tags
        if (this.registeredControlNames && this.registeredControlNames.length > 0) {
            unregisterOwnedControls(this.targetLayer, this.registeredControlNames);
            this.registeredControlNames = [];
        }
    };

    ControllerTransaction.prototype.commit = function() {
        this.committed = true;
        this.newEffects = [];
        this.modifiedValues = [];
        this.newControlDescriptors = [];
        this.modifiedControlDescriptors = [];
        this.registeredControlNames = [];
    };

    return {
        MATCH_NAMES: MATCH_NAMES,
        MASTER_COMMENT_TAG: MASTER_COMMENT_TAG,

        ControllerTransaction: ControllerTransaction,

        isOwnedControl: isOwnedControl,
        registerOwnedControl: registerOwnedControl,
        unregisterOwnedControls: unregisterOwnedControls,

        beginTransaction: function(targetLayer, recipe) {
            return new ControllerTransaction(targetLayer, recipe);
        },

        // Find-only lookup: never creates. Update/Remove must not build a rig
        // as a side effect of locating an existing one.
        findMasterLayer: function(comp) {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!comp) return null;
            for (var i = 1; i <= comp.numLayers; i++) {
                var lyr = comp.layer(i);
                if (lyr) {
                    var comment = lyr.comment || "";
                    if (comment.indexOf(MASTER_COMMENT_TAG) !== -1) return lyr;
                }
            }
            return null;
        },

        getOrCreateMasterLayer: function(comp) {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!comp) return null;

            var foundMaster = this.findMasterLayer(comp);
            if (foundMaster) {
                return foundMaster;
            }

            var baseName = vac34_Config.MASTER_LAYER_NAME;
            var collisionFound = false;
            for (var i = 1; i <= comp.numLayers; i++) {
                var lyr = comp.layer(i);
                if (lyr && lyr.name === baseName) {
                    // User foreign layer with name vac34_Master_Controls but without MASTER_COMMENT_TAG
                    collisionFound = true;
                    break;
                }
            }

            // Create Master Null with collision avoidance
            try {
                var targetName = baseName;
                if (collisionFound || safeFindLayerByName(comp, baseName)) {
                    var counter = 1;
                    while (safeFindLayerByName(comp, baseName + "_" + counter)) {
                        counter++;
                    }
                    targetName = baseName + "_" + counter;
                }

                var master = comp.layers.addNull();
                master.name = targetName;
                try { master.comment = MASTER_COMMENT_TAG; } catch (e) {}
                master.label = 13;
                master.guideLayer = true;
                master._vac34IsNew = true;
                master.moveToBeginning();
                return master;
            } catch (e) {
                return null;
            }
        },

        getEffectPrefixForRecipe: function(recipe) {
            return vac34_Config.EFFECT_PREFIX + recipe.displayName;
        },

        ensureParameterControl: function(targetLayer, recipe, param) {
            if (!targetLayer) return null;
            var effectsGroup = targetLayer.property("ADBE Effect Parade") || targetLayer.property("Effects");
            if (!effectsGroup) return null;

            var effectName = this.getEffectPrefixForRecipe(recipe) + " — " + param.name;
            var expectedMatch = MATCH_NAMES[param.type.toLowerCase()] || "ADBE Slider Control";

            // Check if already exists and verify matchName AND ownership
            var existing = effectsGroup.property(effectName);
            if (existing) {
                if (!isOwnedControl(targetLayer, recipe, existing)) {
                    // Refuse to hijack foreign control
                    return null;
                }
                if (existing.matchName === expectedMatch) {
                    return existing;
                }
                // Name collision with different matchName - cannot safely reuse
                return null;
            }

            try {
                if (effectsGroup.canAddProperty && !effectsGroup.canAddProperty(expectedMatch)) {
                    return null;
                }
                var newEffect = effectsGroup.addProperty(expectedMatch);
                if (newEffect) {
                    newEffect.name = effectName;
                    newEffect._vac34Owned = true;
                    newEffect._vac34RigId = recipe ? recipe.id : "";
                    registerOwnedControl(targetLayer, recipe, newEffect);
                    return newEffect;
                }
            } catch (e) {
                return null;
            }
            return null;
        },

        setupRecipeControls: function(targetLayer, recipe, values) {
            if (!targetLayer || !recipe || !recipe.parameters) return null;
            var tx = new ControllerTransaction(targetLayer, recipe);
            var ok = tx.setup(values);
            if (!ok) {
                tx.rollback();
                return null;
            }
            var controls = tx.controls;
            controls._tx = tx;
            return controls;
        },

        updateParameterValue: function(targetLayer, recipe, paramId, value) {
            if (!targetLayer || !recipe) return false;
            var param = null;
            for (var i = 0; i < recipe.parameters.length; i++) {
                if (recipe.parameters[i].id === paramId) {
                    param = recipe.parameters[i];
                    break;
                }
            }
            if (!param) return false;

            var effectsGroup = targetLayer.property("ADBE Effect Parade") || targetLayer.property("Effects");
            if (!effectsGroup) return false;

            var effectName = this.getEffectPrefixForRecipe(recipe) + " — " + param.name;
            var effect = effectsGroup.property(effectName);
            if (effect) {
                if (!isOwnedControl(targetLayer, recipe, effect)) {
                    return false; // Do not update foreign control!
                }
                var valProp = effect.property(1);
                if (valProp) {
                    try {
                        valProp.setValue(value);
                        if (typeof valProp.value !== "undefined") {
                            return areValuesEqual(valProp.value, value);
                        }
                        return true;
                    } catch (e) {
                        return false;
                    }
                }
            }
            return false;
        },

        removeRecipeControls: function(targetLayer, recipe) {
            if (!targetLayer || !recipe || !recipe.parameters) return 0;
            var effectsGroup = targetLayer.property("ADBE Effect Parade") || targetLayer.property("Effects");
            if (!effectsGroup) return 0;

            var removed = 0;
            var prefix = this.getEffectPrefixForRecipe(recipe);

            // Exact owned-controller discovery: only remove controls that match known parameters AND owned
            var ownedNames = {};
            for (var p = 0; p < recipe.parameters.length; p++) {
                var expectedName = prefix + " — " + recipe.parameters[p].name;
                var expectedMatch = MATCH_NAMES[recipe.parameters[p].type.toLowerCase()] || "ADBE Slider Control";
                ownedNames[expectedName] = expectedMatch;
            }

            var removedNames = [];
            for (var i = effectsGroup.numProperties; i >= 1; i--) {
                var eff = effectsGroup.property(i);
                if (eff && eff.name && ownedNames.hasOwnProperty(eff.name)) {
                    var match = ownedNames[eff.name];
                    if (eff.matchName === match && isOwnedControl(targetLayer, recipe, eff)) {
                        eff.remove();
                        removedNames.push(eff.name);
                        removed++;
                    }
                }
            }

            if (removedNames.length > 0) {
                unregisterOwnedControls(targetLayer, removedNames);
                // Drop the recipe rig tag once no prefixed control of this recipe
                // remains on the layer: a stale tag would keep foreign effects
                // that ever match the prefix classified as owned.
                try {
                    var comment = targetLayer.comment || "";
                    var anyLeft = false;
                    for (var z = 1; z <= effectsGroup.numProperties; z++) {
                        var zEff = effectsGroup.property(z);
                        if (zEff && zEff.name && zEff.name.indexOf(prefix) === 0) { anyLeft = true; break; }
                    }
                    if (!anyLeft && recipe.id) {
                        var rigTag = "/* [vac34_rig:" + recipe.id + "] */";
                        comment = comment.split("\n" + rigTag).join("")
                                        .split(rigTag).join("");
                        targetLayer.comment = comment.replace(/^\s+|\s+$/g, "");
                    }
                } catch (eRig) {}
            }

            return removed;
        }
    };
})();
