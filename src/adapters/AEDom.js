/*
 * vac34_AE — Master Expressions Studio
 * AE DOM Adapter: Safe interaction with After Effects Object Model
 */

var vac34_AEDom = (function() {
    var _undoDepth = 0;
    var _pinnedComp = null;
    var _pinnedCompName = null;
    var _pinnedTarget = null;

    return {
        getActiveComp: function() {
            if (typeof app !== "undefined" && app.project && app.project.activeItem &&
                (typeof CompItem === "undefined" || app.project.activeItem instanceof CompItem)) {
                return app.project.activeItem;
            }
            return null;
        },

        // ---------------------------------------------------------------
        // PIN COMPOSITION
        // A pinned composition never follows the AE viewer focus again. A
        // destroyed or deleted comp is reported, never dereferenced.
        // ---------------------------------------------------------------
        pinComp: function(comp) {
            if (!comp) return { ok: false, error: "NO_COMP", message: "No composition available to pin." };
            _pinnedComp = comp;
            try { _pinnedCompName = comp.name || ""; } catch (eName) { _pinnedCompName = ""; }
            return { ok: true, name: _pinnedCompName };
        },

        isCompPinned: function() {
            return _pinnedComp !== null;
        },

        getPinnedCompName: function() {
            return _pinnedCompName;
        },

        clearCompPin: function() {
            _pinnedComp = null;
            _pinnedCompName = null;
        },

        resolvePinnedComp: function() {
            if (!_pinnedComp) {
                return { ok: false, error: "COMP_NOT_PINNED", message: "Composition is not pinned." };
            }
            var stillInProject = false;
            try {
                if (typeof app !== "undefined" && app.project && app.project.numItems !== undefined) {
                    for (var i = 1; i <= app.project.numItems; i++) {
                        var item = app.project.item(i);
                        if (item === _pinnedComp) { stillInProject = true; break; }
                    }
                } else {
                    stillInProject = true; // no project enumeration available: trust the handle
                }
            } catch (eProj) {
                stillInProject = false;
            }
            if (!stillInProject) {
                var lostName = _pinnedCompName;
                _pinnedComp = null;
                _pinnedTarget = null;
                return {
                    ok: false,
                    error: "PINNED_COMP_MISSING",
                    message: "Pinned composition '" + lostName + "' no longer exists in the project."
                };
            }
            return { ok: true, comp: _pinnedComp, name: _pinnedCompName };
        },

        // ---------------------------------------------------------------
        // PIN TARGET
        // Identity is structural (comp name, layer index+name, effect
        // identity, property index chain, matchName) so the reference is
        // re-resolved on every use, never reused as a stale handle.
        // ---------------------------------------------------------------
        pinTarget: function(comp, prop) {
            if (!comp || !prop) {
                return { ok: false, error: "INVALID_TARGET", message: "No composition or property available to pin." };
            }
            var ownerLyr = (typeof vac34_TargetResolver !== "undefined") ? vac34_TargetResolver.resolveOwnerLayer(prop) : null;
            var descriptor = this.capturePropertyDescriptor(ownerLyr, prop);
            if (!descriptor) {
                return { ok: false, error: "DESCRIPTOR_FAILED", message: "Could not capture property identity for pinning." };
            }
            var valueType = undefined;
            try { valueType = prop.propertyValueType; } catch (eVt) {}
            _pinnedTarget = {
                compName: comp.name || "",
                layerName: ownerLyr ? (ownerLyr.name || "") : "",
                layerIndex: (ownerLyr && ownerLyr.index !== undefined) ? ownerLyr.index : null,
                descriptor: descriptor,
                matchName: prop.matchName || "",
                path: (typeof vac34_TargetResolver !== "undefined") ? vac34_TargetResolver.getPropertyPath(prop) : (descriptor.path || ""),
                propertyValueType: valueType,
                existingRecipeId: this.extractVac34RecipeId(prop),
                hasForeignExpression: this.hasForeignExpression(prop)
            };
            if (_pinnedComp !== comp) {
                _pinnedComp = comp;
                try { _pinnedCompName = comp.name || ""; } catch (eCn) {}
            }
            return { ok: true, path: _pinnedTarget.path };
        },

        isTargetPinned: function() {
            return _pinnedTarget !== null;
        },

        getPinnedTargetInfo: function() {
            if (!_pinnedTarget) return null;
            return {
                compName: _pinnedTarget.compName,
                layerName: _pinnedTarget.layerName,
                path: _pinnedTarget.path,
                matchName: _pinnedTarget.matchName,
                propertyValueType: _pinnedTarget.propertyValueType,
                existingRecipeId: _pinnedTarget.existingRecipeId,
                hasForeignExpression: _pinnedTarget.hasForeignExpression
            };
        },

        clearTargetPin: function() {
            _pinnedTarget = null;
        },

        resolvePinnedTarget: function() {
            if (!_pinnedTarget) {
                return { ok: false, error: "TARGET_NOT_PINNED", message: "Target is not pinned." };
            }
            var compRes = this.resolvePinnedComp();
            if (!compRes.ok) {
                return { ok: false, error: compRes.error, message: compRes.message };
            }
            var comp = compRes.comp;

            var lyr = null;
            var nameHits = [];
            try {
                for (var i = 1; i <= comp.numLayers; i++) {
                    var l = comp.layer(i);
                    if (l === undefined || l === null) continue;
                    if (l.name === _pinnedTarget.layerName) {
                        nameHits.push(l);
                        if (_pinnedTarget.layerIndex === null || l.index === _pinnedTarget.layerIndex) {
                            lyr = l;
                            break;
                        }
                    }
                }
            } catch (eLyr) {
                lyr = null;
                nameHits = [];
            }
            if (!lyr && nameHits.length > 1) {
                // A shifted index with duplicate names is not an identity: fail
                // closed rather than guessing which same-named layer is pinned.
                return {
                    ok: false,
                    error: "PINNED_LAYER_AMBIGUOUS",
                    message: "Pinned target layer '" + _pinnedTarget.layerName + "' matches " + nameHits.length + " layers; layer order changed and identity is ambiguous."
                };
            }
            if (!lyr && nameHits.length === 1) {
                // Index shifted (e.g. a shared master null was inserted at the
                // top): the unique name still identifies the layer unambiguously.
                lyr = nameHits[0];
            }
            if (!lyr) {
                return {
                    ok: false,
                    error: "PINNED_LAYER_MISSING",
                    message: "Pinned target layer '" + _pinnedTarget.layerName + "' not found in composition '" + _pinnedTarget.compName + "'."
                };
            }

            var prop = this.reacquireProperty(lyr, _pinnedTarget.descriptor);
            if (!prop) {
                return {
                    ok: false,
                    error: "PINNED_TARGET_REACQUIRE_FAILED",
                    message: "Pinned property '" + _pinnedTarget.path + "' could not be uniquely reacquired (missing or ambiguous instance)."
                };
            }
            if (_pinnedTarget.matchName && prop.matchName && prop.matchName !== _pinnedTarget.matchName) {
                return {
                    ok: false,
                    error: "PINNED_TARGET_MISMATCH",
                    message: "Pinned property identity mismatch: expected matchName '" + _pinnedTarget.matchName + "'."
                };
            }
            return { ok: true, comp: comp, layer: lyr, prop: prop, path: _pinnedTarget.path };
        },

        getSelectedLayers: function(comp) {
            if (!comp) comp = this.getActiveComp();
            if (!comp) return [];
            var layers = [];
            for (var i = 0; i < comp.selectedLayers.length; i++) {
                layers.push(comp.selectedLayers[i]);
            }
            return layers;
        },

        beginUndo: function(name) {
            try {
                if (_undoDepth === 0 && typeof app !== "undefined" && app.beginUndoGroup) {
                    app.beginUndoGroup(name || "vac34_AE Action");
                }
                _undoDepth++;
            } catch (e) {
                _undoDepth = 0;
            }
        },

        endUndo: function() {
            try {
                if (_undoDepth > 0) {
                    _undoDepth--;
                    if (_undoDepth === 0 && typeof app !== "undefined" && app.endUndoGroup) {
                        app.endUndoGroup();
                    }
                }
            } catch (e) {
                _undoDepth = 0;
            }
        },

        getUndoDepth: function() {
            return _undoDepth;
        },

        resolveProperty: function(layer, propPath) {
            if (!layer) return null;
            var parts = propPath.split(".");
            var current = layer;
            for (var i = 0; i < parts.length; i++) {
                var p = parts[i];
                try {
                    if (current.property) {
                        current = current.property(p);
                    } else {
                        return null;
                    }
                } catch (e) {
                    return null;
                }
                if (!current) return null;
            }
            return current;
        },

        canSetExpression: function(prop) {
            if (!prop) return false;
            try {
                if (prop.dimensionsSeparated === true) {
                    return false;
                }
                return (prop.canSetExpression === true);
            } catch (e) {
                return false;
            }
        },

        isVac34Expression: function(prop) {
            if (!prop || !prop.expression) return false;
            var expr = prop.expression.replace(/^\s+/, "");
            return (expr.indexOf(vac34_Config.TAG_PREFIX) === 0);
        },

        extractVac34RecipeId: function(prop) {
            if (!prop || !prop.expression) return null;
            var expr = prop.expression.replace(/^\s+/, "");
            if (expr.indexOf(vac34_Config.TAG_PREFIX) !== 0) return null;
            var start = vac34_Config.TAG_PREFIX.length;
            var end = expr.indexOf(vac34_Config.TAG_SUFFIX, start);
            if (end !== -1) {
                return expr.substring(start, end).replace(/^\s+|\s+$/g, "");
            }
            return null;
        },

        findRecipeProperties: function(layer, recipeId) {
            var found = [];
            if (!layer || typeof layer.property !== "function") return found;
            var self = this;

            function searchGroup(group) {
                if (!group || !group.numProperties) return;
                for (var i = 1; i <= group.numProperties; i++) {
                    try {
                        var p = group.property(i);
                        if (!p) continue;
                        if (self.canSetExpression(p)) {
                            if (self.isVac34Expression(p)) {
                                if (!recipeId || self.extractVac34RecipeId(p) === recipeId) {
                                    found.push(p);
                                }
                            }
                        } else if (p.numProperties && p.numProperties > 0) {
                            searchGroup(p);
                        }
                    } catch (e) {}
                }
            }

            var xform = layer.property("Transform");
            if (xform) searchGroup(xform);

            var effects = layer.property("ADBE Effect Parade") || layer.property("Effects");
            if (effects) searchGroup(effects);

            return found;
        },

        findRecipeProperty: function(layer, recipeId) {
            var props = this.findRecipeProperties(layer, recipeId);
            return (props.length > 0) ? props[0] : null;
        },

        hasForeignExpression: function(prop) {
            if (!prop || !prop.expression) return false;
            var trimmed = prop.expression.replace(/^\s+|\s+$/g, "");
            if (trimmed === "") return false;
            return !this.isVac34Expression(prop);
        },

        classifyExpression: function(prop, targetRecipeId) {
            if (!prop || !prop.expression) return { state: "NONE", recipeId: null };
            var expr = prop.expression.replace(/^\s+|\s+$/g, "");
            if (expr === "") return { state: "NONE", recipeId: null };
            if (!this.isVac34Expression(prop)) {
                return { state: "FOREIGN", recipeId: null, expression: expr };
            }
            var existingRecipeId = this.extractVac34RecipeId(prop);
            if (!existingRecipeId) {
                return { state: "DAMAGED", recipeId: null };
            }
            if (!targetRecipeId || existingRecipeId === targetRecipeId) {
                return { state: "SAME_RECIPE", recipeId: existingRecipeId };
            }
            return { state: "DIFFERENT_RECIPE", recipeId: existingRecipeId };
        },

        verifyExpressionState: function(prop) {
            if (!prop) return { ok: false, error: "Property reference is null" };
            try {
                if (prop.expressionError && prop.expressionError.length > 0) {
                    return { ok: false, error: prop.expressionError };
                }
                if (prop.canSetExpression && prop.expression && prop.expression.length > 0 && prop.expressionEnabled === false) {
                    return { ok: false, error: "Expression was disabled by host due to error." };
                }
                return { ok: true, error: null };
            } catch (e) {
                return { ok: false, error: e.message || String(e) };
            }
        },

        capturePropertyDescriptor: function(layer, prop) {
            if (!prop) return null;
            var ownerLyr = layer;
            if (!ownerLyr && typeof vac34_TargetResolver !== "undefined") {
                ownerLyr = vac34_TargetResolver.resolveOwnerLayer(prop);
            }

            var pathParts = [];
            var indexPath = [];
            var cur = prop;
            var effectNode = null;
            var effectIndex = -1;
            var effectMatchName = "";
            var effectName = "";
            var guard = 25;

            while (cur && guard-- > 0) {
                if (cur.propertyIndex !== undefined) {
                    indexPath.unshift(cur.propertyIndex);
                } else if (cur.name) {
                    indexPath.unshift(cur.name);
                }
                if (cur.name) {
                    pathParts.unshift(cur.name);
                }
                try {
                    var parent = cur.parentProperty;
                    if (!parent) break;
                    var parentName = parent.name || "";
                    var parentMatch = parent.matchName || "";
                    if (parentMatch === "ADBE Effect Parade" || parentName === "Effects" || parentName === "ADBE Effect Parade") {
                        effectNode = cur;
                        effectIndex = (cur.propertyIndex !== undefined) ? cur.propertyIndex : -1;
                        effectMatchName = cur.matchName || "";
                        effectName = cur.name || "";
                    }
                    if (ownerLyr && (parent === ownerLyr || cur === ownerLyr)) break;
                    cur = parent;
                } catch (e) {
                    break;
                }
            }

            var subChain = [];
            if (effectNode) {
                var c = prop;
                var g2 = 15;
                while (c && c !== effectNode && g2-- > 0) {
                    if (c.propertyIndex !== undefined) {
                        subChain.unshift(c.propertyIndex);
                    } else if (c.name) {
                        subChain.unshift(c.name);
                    }
                    c = c.parentProperty;
                }
            }

            return {
                layerIndex: ownerLyr ? (ownerLyr.index !== undefined ? ownerLyr.index : null) : null,
                layerName: ownerLyr ? (ownerLyr.name || "") : "",
                name: prop.name || "",
                matchName: prop.matchName || "",
                path: pathParts.join(" > "),
                indexPath: indexPath,
                isEffect: !!effectNode,
                effectIndex: effectIndex,
                effectMatchName: effectMatchName,
                effectName: effectName,
                subChain: subChain
            };
        },

        reacquireProperty: function(layer, descriptor) {
            if (!layer || !descriptor) return null;
            try {
                if (descriptor.isEffect) {
                    var effectsGroup = layer.property("ADBE Effect Parade") || layer.property("Effects");
                    if (!effectsGroup) return null;

                    function descriptorNameMatches(e) {
                        if (!e) return false;
                        var mOk = !descriptor.effectMatchName || e.matchName === descriptor.effectMatchName;
                        var nOk = !descriptor.effectName || e.name === descriptor.effectName;
                        return mOk && nOk;
                    }

                    var eff = null;
                    // 1. Try by verified original effectIndex
                    if (descriptor.effectIndex > 0 && descriptor.effectIndex <= effectsGroup.numProperties) {
                        var candidate = effectsGroup.property(descriptor.effectIndex);
                        if (descriptorNameMatches(candidate)) {
                            eff = candidate;
                        }
                    }

                    // 2. No index-verified hit: name+matchName are NOT unique identity.
                    //    Accept only a sole, unambiguous matching instance; duplicates fail closed.
                    if (!eff && effectsGroup.numProperties) {
                        var soleMatch = null;
                        var matchCount = 0;
                        for (var i = 1; i <= effectsGroup.numProperties; i++) {
                            var e = effectsGroup.property(i);
                            if (descriptorNameMatches(e)) {
                                matchCount++;
                                soleMatch = e;
                            }
                        }
                        eff = (matchCount === 1) ? soleMatch : null;
                    }

                    if (!eff) return null;

                    // Navigate subChain from effect down to the target property
                    var target = eff;
                    if (descriptor.subChain && descriptor.subChain.length > 0) {
                        for (var s = 0; s < descriptor.subChain.length; s++) {
                            var subKey = descriptor.subChain[s];
                            if (typeof target.property === "function") {
                                target = target.property(subKey);
                            } else {
                                target = null;
                                break;
                            }
                            if (!target) break;
                        }
                    }
                    if (target) {
                        if (descriptor.matchName && target.matchName && target.matchName !== descriptor.matchName) {
                            return null;
                        }
                        return target;
                    }
                    return null;
                }

                // Transform or layer-level property: navigate indexPath
                var current = layer;
                if (descriptor.indexPath && descriptor.indexPath.length > 0) {
                    for (var p = 0; p < descriptor.indexPath.length; p++) {
                        if (typeof current.property === "function") {
                            current = current.property(descriptor.indexPath[p]);
                        } else {
                            current = null;
                            break;
                        }
                        if (!current) break;
                    }
                    if (current) return current;
                }

                return null;
            } catch (err) {
                return null;
            }
        },

        isLayer3D: function(layer) {
            if (!layer) return false;
            try {
                return (layer.threeDLayer === true);
            } catch (e) {
                return false;
            }
        },

        getPropertyDimension: function(layer, prop) {
            if (!prop) return 0;
            try {
                if (typeof PropertyValueType !== "undefined") {
                    if (prop.propertyValueType === PropertyValueType.OneD) return 1;
                    if (prop.propertyValueType === PropertyValueType.TwoD || prop.propertyValueType === PropertyValueType.TwoD_SPATIAL) {
                        if (this.isLayer3D(layer)) {
                            var mName = prop.matchName || "";
                            if (mName === "ADBE Position" || mName === "ADBE Scale" || mName === "ADBE Anchor Point") {
                                return 3;
                            }
                        }
                        return 2;
                    }
                    if (prop.propertyValueType === PropertyValueType.ThreeD || prop.propertyValueType === PropertyValueType.ThreeD_SPATIAL) return 3;
                    if (prop.propertyValueType === PropertyValueType.COLOR) return 4;
                    if (prop.propertyValueType === PropertyValueType.TEXT_DOCUMENT) return "text";
                }
                // Fallbacks
                if (prop.propertyValueType === 1) return 1;
                if (prop.propertyValueType === 2) {
                    if (this.isLayer3D(layer)) return 3;
                    return 2;
                }
                if (prop.propertyValueType === 3) return 3;
                if (prop.propertyValueType === 4) return 4;
                if (prop.propertyValueType === 7) return "text";

                if (prop.value instanceof Array) {
                    return prop.value.length;
                }
                if (typeof prop.value === "number") return 1;
                if (typeof prop.value === "string") return "text";
            } catch (e) {}
            return 1;
        }
    };
})();
