/*
 * vac34_AE — Master Expressions Studio
 * Diagnostics: Strict compatibility checks, property dimension validation, foreign & cross-recipe conflict enforcement
 */

var vac34_Diagnostics = (function() {
    var _startupStages = {
        STAGE_1: "1. Script loaded",
        STAGE_2: "2. Modules initialized",
        STAGE_3: "3. UI container created",
        STAGE_4: "4. Controls created",
        STAGE_5: "5. Recipes loaded",
        STAGE_6: "6. Initial layout complete",
        STAGE_7: "7. Panel ready"
    };
    var _currentStartupStage = _startupStages.STAGE_2;
    var _startupLog = [
        { stage: _startupStages.STAGE_1, timestamp: (new Date()).getTime() },
        { stage: _startupStages.STAGE_2, timestamp: (new Date()).getTime() }
    ];
    var _startupError = null;

    function _writePersistentLog(entryText) {
        try {
            if (typeof Folder !== "undefined" && typeof File !== "undefined") {
                var userDir = (Folder.userData && Folder.userData.fsName) ? Folder.userData.fsName : (Folder.temp ? Folder.temp.fsName : "");
                if (userDir) {
                    var targetDir = new Folder(userDir + "/vac34_AE");
                    if (!targetDir.exists) {
                        targetDir.create();
                    }
                    var logFile = new File(targetDir.fsName + "/startup_diagnostics.log");
                    logFile.open("a");
                    var ts = (new Date()).toISOString ? (new Date()).toISOString() : String(new Date());
                    var hostVer = (typeof app !== "undefined" && app.version) ? app.version : "UnknownHost";
                    var buildId = (typeof vac34_Config !== "undefined" && vac34_Config.BUILD_ID) ? vac34_Config.BUILD_ID : "0";
                    logFile.writeln("[" + ts + "] [Host:" + hostVer + "] [Build:" + buildId + "] " + entryText);
                    logFile.close();
                }
            } else if (typeof require !== "undefined") {
                try {
                    var fs = require("fs");
                    var path = require("path");
                    var os = require("os");
                    var logPath = path.join(os.tmpdir(), "vac34_ae_startup_diagnostics.log");
                    var tsNode = new Date().toISOString();
                    fs.appendFileSync(logPath, "[" + tsNode + "] " + entryText + "\n");
                } catch (ne) {}
            }
        } catch (e) {}
    }

    return {
        getStartupStages: function() {
            return _startupStages;
        },

        setStartupStage: function(stage) {
            _currentStartupStage = stage;
            _startupLog.push({ stage: stage, timestamp: (new Date()).getTime() });
            _writePersistentLog("STAGE: " + stage);
        },

        getCurrentStartupStage: function() {
            return _currentStartupStage;
        },

        getStartupLog: function() {
            return _startupLog;
        },

        writePersistentLog: function(entryText) {
            _writePersistentLog(entryText);
        },

        recordStartupError: function(stage, err) {
            _currentStartupStage = stage;
            _startupError = {
                stage: stage,
                message: (err && (err.message || err.toString())) || "Unknown initialization error",
                line: (err && err.line) ? err.line : null,
                fileName: (err && err.fileName) ? err.fileName : null
            };
            _startupLog.push({
                stage: stage,
                error: _startupError.message,
                line: _startupError.line,
                timestamp: (new Date()).getTime()
            });
            _writePersistentLog("ERROR at [" + stage + "]: " + _startupError.message + (_startupError.line ? (" (line " + _startupError.line + ")") : ""));
        },

        getStartupError: function() {
            return _startupError;
        },

        isStartupSuccessful: function() {
            return _startupError === null && _currentStartupStage === _startupStages.STAGE_7;
        },
        isDimensionCompatible: function(expectedDim, actualDim) {
            if (!expectedDim) return true;
            if (expectedDim === actualDim) return true;
            // Adaptive vector: 2D recipe can adapt to 3D layer vector properties [x, y, z]
            if (expectedDim === 2 && actualDim === 3) return true;
            if (expectedDim instanceof Array) {
                for (var d = 0; d < expectedDim.length; d++) {
                    if (expectedDim[d] === actualDim) return true;
                }
                return false;
            }
            return false;
        },

        checkApplication: function(comp, layers, recipe, targetPropPath) {
            var result = {
                canApply: false,
                warnings: [],
                errors: [],
                compatibleLayers: [],
                conflictedLayers: [],
                incompatibleLayers: []
            };

            if (!comp) {
                result.errors.push("No active composition open in After Effects.");
                return result;
            }

            if (!layers || layers.length === 0) {
                result.errors.push("No layer selected. Select at least one layer.");
                return result;
            }

            if (!recipe) {
                result.errors.push("No recipe selected.");
                return result;
            }

            // Check Audio dependency
            if (recipe.requiresAudio) {
                var audioLayers = vac34_AudioEngine.findAudioLayers(comp);
                if (audioLayers.length === 0) {
                    result.warnings.push("Warning: No 'Audio Amplitude' layer found in active composition. (Expression will use fallback amplitude 0 until audio layer is created).");
                }
            }

            // Inspect selected layers
            for (var i = 0; i < layers.length; i++) {
                var lyr = layers[i];
                var propPath = targetPropPath || (recipe.targetProperties ? recipe.targetProperties[0] : null);

                if (!propPath || propPath === "Any.Property") {
                    var candidateProp = null;
                    if (lyr.selectedProperties && lyr.selectedProperties.length > 0) {
                        for (var sp = 0; sp < lyr.selectedProperties.length; sp++) {
                            if (vac34_AEDom.canSetExpression(lyr.selectedProperties[sp])) {
                                candidateProp = lyr.selectedProperties[sp];
                                break;
                            }
                        }
                    }
                    if (!candidateProp) {
                        candidateProp = lyr.property("Transform") ? lyr.property("Transform").property("Position") : null;
                    }

                    if (!candidateProp || !vac34_AEDom.canSetExpression(candidateProp)) {
                        result.incompatibleLayers.push(lyr);
                        result.warnings.push("Layer '" + lyr.name + "' has no property capable of receiving expressions.");
                        continue;
                    }

                    // STRICT P1: Property dimension compatibility check
                    var candDim = vac34_AEDom.getPropertyDimension(lyr, candidateProp);
                    if (recipe.targetDimensions && !this.isDimensionCompatible(recipe.targetDimensions, candDim)) {
                        result.incompatibleLayers.push(lyr);
                        result.warnings.push("Layer '" + lyr.name + "' property dimension mismatch: recipe expects " + recipe.targetDimensions + "D, property has dimension " + candDim + ".");
                        continue;
                    }

                    // Foreign expression check
                    if (vac34_AEDom.hasForeignExpression(candidateProp)) {
                        result.conflictedLayers.push(lyr);
                        result.warnings.push("CONFLICT: Layer '" + lyr.name + "' has an existing foreign expression. Skipped to prevent overwrite.");
                        continue;
                    }

                    // Cross-recipe conflict check
                    if (vac34_AEDom.isVac34Expression(candidateProp)) {
                        var existingId = vac34_AEDom.extractVac34RecipeId(candidateProp);
                        if (existingId !== null && existingId !== recipe.id) {
                            result.conflictedLayers.push(lyr);
                            result.warnings.push("CONFLICT: Layer '" + lyr.name + "' already has active vac34 behavior '" + existingId + "'. Refusing silent replacement.");
                            continue;
                        }
                    }

                    result.compatibleLayers.push(lyr);
                    continue;
                }

                var prop = vac34_AEDom.resolveProperty(lyr, propPath);
                if (!prop) {
                    result.incompatibleLayers.push(lyr);
                    result.warnings.push("Layer '" + lyr.name + "' lacks target property '" + propPath + "'.");
                    continue;
                }

                if (!vac34_AEDom.canSetExpression(prop)) {
                    result.incompatibleLayers.push(lyr);
                    result.warnings.push("Layer '" + lyr.name + "' property '" + propPath + "' cannot receive expressions.");
                    continue;
                }

                // STRICT P1: Property dimension compatibility check
                var actualDim = vac34_AEDom.getPropertyDimension(lyr, prop);
                if (recipe.targetDimensions && !this.isDimensionCompatible(recipe.targetDimensions, actualDim)) {
                    result.incompatibleLayers.push(lyr);
                    result.warnings.push("Layer '" + lyr.name + "' property '" + propPath + "' dimension mismatch: recipe expects " + recipe.targetDimensions + "D, property has dimension " + actualDim + ".");
                    continue;
                }

                // STRICT P0: Foreign expression protection
                if (vac34_AEDom.hasForeignExpression(prop)) {
                    result.conflictedLayers.push(lyr);
                    result.warnings.push("CONFLICT: Layer '" + lyr.name + "' property '" + propPath + "' already has a custom expression. Refusing to overwrite (skipped).");
                    continue;
                }

                // STRICT P0: Cross-recipe overwrite protection
                if (vac34_AEDom.isVac34Expression(prop)) {
                    var activeId = vac34_AEDom.extractVac34RecipeId(prop);
                    if (activeId !== null && activeId !== recipe.id) {
                        result.conflictedLayers.push(lyr);
                        result.warnings.push("CONFLICT: Layer '" + lyr.name + "' property '" + propPath + "' already has active vac34 behavior '" + activeId + "'. Refusing silent replacement.");
                        continue;
                    }
                }

                result.compatibleLayers.push(lyr);
            }

            if (result.compatibleLayers.length > 0) {
                result.canApply = true;
            } else {
                result.canApply = false;
                if (result.conflictedLayers.length > 0) {
                    result.errors.push("Application aborted: " + result.conflictedLayers.length + " layer(s) have conflicting expressions.");
                } else {
                    result.errors.push("None of the selected layers have compatible properties for '" + recipe.displayName + "'.");
                }
            }

            return result;
        }
    };
})();