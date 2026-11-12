/*
 * vac34_AE — Master Expressions Studio
 * TargetResolver: Universal Selected-Property Target Resolution & Compatibility Engine
 */

var vac34_TargetResolver = (function() {
    var TARGET_MODES = {
        AUTO: "AUTO",
        SELECTED: "SELECTED_PROPERTY",
        DEFAULT: "RECIPE_DEFAULT"
    };

    var _currentTargetMode = TARGET_MODES.AUTO;

    function resolveOwnerLayer(prop) {
        if (!prop) return null;
        try {
            if (prop.propertyDepth && typeof prop.propertyGroup === "function") {
                var top = prop.propertyGroup(prop.propertyDepth);
                if (top && typeof top.property === "function") {
                    return top;
                }
            }
        } catch (e) {}

        var current = prop;
        var guard = 20;
        while (current && guard-- > 0) {
            try {
                if (current.parentProperty) {
                    current = current.parentProperty;
                } else if (typeof current.property === "function" && (current.containingComp !== undefined || current.numProperties !== undefined)) {
                    return current;
                } else {
                    break;
                }
            } catch (e2) {
                break;
            }
        }

        if (current && current !== prop && typeof current.property === "function") {
            return current;
        }
        return null;
    }

    function getPropertyPath(prop) {
        if (!prop) return "None";
        var parts = [prop.name || "Property"];
        var current = prop;
        var guard = 15;
        while (current && guard-- > 0) {
            try {
                if (current.parentProperty) {
                    current = current.parentProperty;
                    if (current && current.name) {
                        parts.unshift(current.name);
                    }
                } else {
                    break;
                }
            } catch (e) {
                break;
            }
        }
        return parts.join(" > ");
    }

    function getPropertyUniqueKey(layer, prop) {
        if (!prop) return "";
        var lyr = layer || resolveOwnerLayer(prop);
        var lyrKey = lyr ? ("L_" + (lyr.index !== undefined ? lyr.index : (lyr.id || lyr.name))) : "L_unknown";
        var idxChain = [];
        var cur = prop;
        var guard = 20;
        while (cur && guard-- > 0) {
            if (lyr && cur === lyr) break;
            var idx = (cur.propertyIndex !== undefined) ? cur.propertyIndex : (cur.name || "0");
            idxChain.unshift(idx);
            try {
                if (!cur.parentProperty) break;
                cur = cur.parentProperty;
            } catch (e) {
                break;
            }
        }
        var mName = prop.matchName || prop.name || "";
        return lyrKey + ":" + idxChain.join("/") + ":" + mName;
    }

    function getSelectedProperties(comp) {
        if (!comp) comp = vac34_AEDom.getActiveComp();
        if (!comp) return [];

        var props = [];
        var seenKeys = {};
        var seenObjects = [];

        function addProp(p, ownerLyr) {
            if (!p || !vac34_AEDom.canSetExpression(p)) return;
            // 1. Direct object identity deduplication
            for (var o = 0; o < seenObjects.length; o++) {
                if (seenObjects[o] === p) return;
            }
            // 2. Stable structural identity deduplication
            var lyr = ownerLyr || resolveOwnerLayer(p);
            var key = getPropertyUniqueKey(lyr, p);
            if (key && seenKeys[key]) return;
            if (key) seenKeys[key] = true;

            seenObjects.push(p);
            props.push(p);
        }

        // 1. Try comp.selectedProperties if host supports it
        try {
            if (comp.selectedProperties && comp.selectedProperties.length > 0) {
                for (var i = 0; i < comp.selectedProperties.length; i++) {
                    addProp(comp.selectedProperties[i], null);
                }
            }
        } catch (eComp) {}

        // 2. Search across comp.selectedLayers
        if (comp.selectedLayers && comp.selectedLayers.length > 0) {
            for (var l = 0; l < comp.selectedLayers.length; l++) {
                var lyr = comp.selectedLayers[l];
                if (lyr && lyr.selectedProperties && lyr.selectedProperties.length > 0) {
                    for (var sp = 0; sp < lyr.selectedProperties.length; sp++) {
                        addProp(lyr.selectedProperties[sp], lyr);
                    }
                }
            }
        }

        return props;
    }

    function inspectProperty(layer, prop) {
        if (!prop) return null;
        var ownerLyr = layer || resolveOwnerLayer(prop);
        var dim = vac34_AEDom.getPropertyDimension(ownerLyr, prop);
        var canSet = vac34_AEDom.canSetExpression(prop);
        var hasForeign = vac34_AEDom.hasForeignExpression(prop);
        var isVac = vac34_AEDom.isVac34Expression(prop);
        var val = null;
        try { val = prop.value; } catch (e) {}

        return {
            prop: prop,
            layer: ownerLyr,
            name: prop.name || "",
            matchName: prop.matchName || "",
            path: getPropertyPath(prop),
            propertyValueType: prop.propertyValueType,
            dimension: dim,
            canSetExpression: canSet,
            hasForeignExpression: hasForeign,
            isVac34: isVac,
            currentValue: val
        };
    }

    function checkPropertyCompatibility(inspected, recipe) {
        if (!inspected || !inspected.prop) {
            return { compatible: false, reason: "No property selected." };
        }
        if (!inspected.canSetExpression) {
            return { compatible: false, reason: "Property does not support expressions (canSetExpression is false)." };
        }
        if (!recipe) {
            return { compatible: false, reason: "No recipe selected." };
        }

        // P0: 0 is a valid enum value (dimension-agnostic), never a truthy fallback to 2
        var expectedDim = recipe.targetDimensions;
        if (expectedDim === undefined || expectedDim === null || expectedDim === "") {
            expectedDim = 2;
        }
        var actualDim = inspected.dimension;

        function dimLabel(d) {
            return (d === "text") ? "text" : (d + "D");
        }

        function isNumericDim(d) {
            return d === 1 || d === 2 || d === 3 || d === 4;
        }

        // Special case: Universal Audio Mapper accepts any 1D scalar
        if (recipe.id === "audio.property.map.scalar") {
            if (actualDim === 1) {
                return { compatible: true, reason: "Compatible 1D numeric property." };
            } else {
                return { compatible: false, reason: "Recipe requires 1D scalar property, but property is " + dimLabel(actualDim) + "." };
            }
        }

        // Dimension-agnostic (0): any numerically dimensioned property; nonnumeric
        // types (text, and props the host refuses expressions on) are rejected.
        if (expectedDim === 0) {
            if (isNumericDim(actualDim)) {
                return { compatible: true, reason: "Compatible numeric property (" + dimLabel(actualDim) + ")." };
            }
            return { compatible: false, reason: "Universal recipe requires a numeric property, but selected property is " + dimLabel(actualDim) + "." };
        }

        // Generic 1D recipes
        if (expectedDim === 1) {
            if (actualDim === 1) {
                return { compatible: true, reason: "Compatible 1D property." };
            } else {
                return { compatible: false, reason: "Recipe expects 1D property, but selected property is " + dimLabel(actualDim) + "." };
            }
        }

        // 2D recipes (e.g. Scale, Position)
        if (expectedDim === 2) {
            if (actualDim === 2 || actualDim === 3) {
                return { compatible: true, reason: "Compatible 2D/3D spatial property." };
            } else {
                return { compatible: false, reason: "Recipe expects 2D vector, but selected property is " + dimLabel(actualDim) + " (" + inspected.name + ")." };
            }
        }

        if (actualDim === expectedDim) {
            return { compatible: true, reason: "Compatible dimensions." };
        }

        return { compatible: false, reason: "Dimension mismatch: recipe expects " + expectedDim + "D, property is " + dimLabel(actualDim) + "." };
    }

    function resolveTargets(comp, layers, recipe, targetMode) {
        var mode = targetMode || _currentTargetMode;
        if (!comp) comp = vac34_AEDom.getActiveComp();
        if (!layers) layers = vac34_AEDom.getSelectedLayers(comp);

        var selectedProps = getSelectedProperties(comp);
        var resolvedTargets = [];
        var incompatibleCount = 0;

        // MODE 1: SELECTED_PROPERTY (Strict)
        if (mode === TARGET_MODES.SELECTED) {
            if (selectedProps.length === 0) {
                return {
                    ok: false,
                    targets: [],
                    compatibleCount: 0,
                    incompatibleCount: 0,
                    message: "Cannot apply: No properties selected in Selected Property mode."
                };
            }

            for (var i = 0; i < selectedProps.length; i++) {
                var p = selectedProps[i];
                var lyr = resolveOwnerLayer(p) || (layers && layers[0]);
                var insp = inspectProperty(lyr, p);
                var compCheck = checkPropertyCompatibility(insp, recipe);
                if (compCheck.compatible) {
                    resolvedTargets.push({
                        layer: lyr,
                        prop: p,
                        descriptor: vac34_AEDom.capturePropertyDescriptor(lyr, p),
                        inspected: insp,
                        path: insp.path
                    });
                } else {
                    incompatibleCount++;
                }
            }

            if (resolvedTargets.length === 0) {
                return {
                    ok: false,
                    targets: [],
                    compatibleCount: 0,
                    incompatibleCount: incompatibleCount,
                    message: "Cannot apply: selected property is incompatible with " + (recipe ? recipe.displayName : "behavior") + "."
                };
            }

            return {
                ok: true,
                targets: resolvedTargets,
                compatibleCount: resolvedTargets.length,
                incompatibleCount: incompatibleCount,
                message: "Resolved " + resolvedTargets.length + " target properties."
            };
        }

        // MODE 2: RECIPE_DEFAULT
        if (mode === TARGET_MODES.DEFAULT) {
            var targetPath = (recipe && recipe.targetProperties && recipe.targetProperties[0]) ? recipe.targetProperties[0] : "Transform.Position";
            if (!layers || layers.length === 0) {
                return { ok: false, targets: [], message: "Cannot apply: No layers selected." };
            }
            for (var lIdx = 0; lIdx < layers.length; lIdx++) {
                var dLyr = layers[lIdx];
                var dProp = vac34_AEDom.resolveProperty(dLyr, targetPath);
                if (dProp) {
                    var dInsp = inspectProperty(dLyr, dProp);
                    resolvedTargets.push({
                        layer: dLyr,
                        prop: dProp,
                        descriptor: vac34_AEDom.capturePropertyDescriptor(dLyr, dProp),
                        inspected: dInsp,
                        path: dInsp ? dInsp.path : (dLyr.name + " > " + targetPath)
                    });
                }
            }
            return {
                ok: resolvedTargets.length > 0,
                targets: resolvedTargets,
                compatibleCount: resolvedTargets.length,
                incompatibleCount: 0,
                message: "Resolved " + resolvedTargets.length + " default recipe targets."
            };
        }

        // MODE 3: AUTO (Intuitive)
        // If compatible properties are explicitly selected, prioritize them!
        if (selectedProps.length > 0) {
            for (var s = 0; s < selectedProps.length; s++) {
                var sProp = selectedProps[s];
                var sLyr = resolveOwnerLayer(sProp) || (layers && layers[0]);
                var sInsp = inspectProperty(sLyr, sProp);
                var sCheck = checkPropertyCompatibility(sInsp, recipe);
                if (sCheck.compatible) {
                    resolvedTargets.push({
                        layer: sLyr,
                        prop: sProp,
                        descriptor: vac34_AEDom.capturePropertyDescriptor(sLyr, sProp),
                        inspected: sInsp,
                        path: sInsp.path
                    });
                } else {
                    incompatibleCount++;
                }
            }

            if (resolvedTargets.length > 0) {
                return {
                    ok: true,
                    targets: resolvedTargets,
                    compatibleCount: resolvedTargets.length,
                    incompatibleCount: incompatibleCount,
                    message: "Targeting " + resolvedTargets.length + " selected properties."
                };
            }

            // User explicitly selected properties, but ALL of them are incompatible!
            // P0 requirement: Never silently substitute incompatible target!
            return {
                ok: false,
                targets: [],
                compatibleCount: 0,
                incompatibleCount: incompatibleCount,
                message: "Cannot apply: selected property is incompatible with " + (recipe ? recipe.displayName : "behavior") + "."
            };
        }

        // No properties explicitly selected: fallback to recipe default
        var autoPath = (recipe && recipe.targetProperties && recipe.targetProperties[0]) ? recipe.targetProperties[0] : "Transform.Position";
        if (layers && layers.length > 0) {
            for (var a = 0; a < layers.length; a++) {
                var aLyr = layers[a];
                var aProp = vac34_AEDom.resolveProperty(aLyr, autoPath);
                if (aProp) {
                    var aInsp = inspectProperty(aLyr, aProp);
                    resolvedTargets.push({
                        layer: aLyr,
                        prop: aProp,
                        descriptor: vac34_AEDom.capturePropertyDescriptor(aLyr, aProp),
                        inspected: aInsp,
                        path: aInsp ? aInsp.path : (aLyr.name + " > " + autoPath)
                    });
                }
            }
        }

        return {
            ok: resolvedTargets.length > 0,
            targets: resolvedTargets,
            compatibleCount: resolvedTargets.length,
            incompatibleCount: 0,
            message: "Targeting recipe default (" + autoPath + ")."
        };
    }

    function getPreviewSummary(comp, layers, recipe, targetMode) {
        var res = resolveTargets(comp, layers, recipe, targetMode);
        if (!res.ok) {
            if (res.incompatibleCount > 0) {
                return "Incompatible selection (" + res.incompatibleCount + " rejected)";
            }
            return "No target resolved";
        }
        if (res.targets.length === 1) {
            return "Target: " + res.targets[0].path;
        }
        if (res.targets.length > 1) {
            return "Targets: " + res.compatibleCount + " compatible" + (res.incompatibleCount > 0 ? (" / " + res.incompatibleCount + " incompatible") : "");
        }
        return "Target: None";
    }

    return {
        TARGET_MODES: TARGET_MODES,
        getTargetMode: function() { return _currentTargetMode; },
        setTargetMode: function(m) { _currentTargetMode = m; },
        resolveOwnerLayer: resolveOwnerLayer,
        getPropertyPath: getPropertyPath,
        getPropertyUniqueKey: getPropertyUniqueKey,
        getSelectedProperties: getSelectedProperties,
        inspectProperty: inspectProperty,
        checkPropertyCompatibility: checkPropertyCompatibility,
        resolveTargets: resolveTargets,
        getPreviewSummary: getPreviewSummary
    };
})();
