/*
 * vac34_AE — Master Expressions Studio
 * AudioEngine: Audio source discovery, channel routing & temporal envelope generation
 */

var vac34_AudioEngine = (function() {
    function escapeStringLiteral(str) {
        if (str === null || str === undefined) return '""';
        str = String(str);
        return '"' + str.replace(/\\/g, '\\\\')
                        .replace(/"/g, '\\"')
                        .replace(/\n/g, '\\n')
                        .replace(/\r/g, '\\r')
                        .replace(/\t/g, '\\t')
                        .replace(/[\x00-\x1f]/g, function(c) {
                            var hex = c.charCodeAt(0).toString(16);
                            return '\\u' + ('0000' + hex).slice(-4);
                        }) + '"';
    }

    return {
        escapeStringLiteral: escapeStringLiteral,

        findAudioLayers: function(comp) {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!comp) return [];
            var found = [];
            for (var i = 1; i <= comp.numLayers; i++) {
                var l = comp.layer(i);
                // Check if name contains audio or if it has Audio Amplitude effects
                var effects = l.property("ADBE Effect Parade") || l.property("Effects");
                var hasAudioSliders = false;
                if (effects) {
                    if (effects.property("Both Channels") || effects.property("Left Channel") || effects.property("Right Channel")) {
                        hasAudioSliders = true;
                    }
                }
                if (l.name === vac34_Config.AUDIO_LAYER_NAME || hasAudioSliders) {
                    found.push({
                        index: i,
                        name: l.name,
                        layer: l,
                        hasBoth: !!(effects && effects.property("Both Channels")),
                        hasLeft: !!(effects && effects.property("Left Channel")),
                        hasRight: !!(effects && effects.property("Right Channel"))
                    });
                }
            }
            return found;
        },

        getPrimaryAudioLayerName: function(comp) {
            var layers = this.findAudioLayers(comp);
            if (layers.length > 0) {
                return layers[0].name;
            }
            return vac34_Config.AUDIO_LAYER_NAME;
        },

        validateAudioSource: function(comp, audioLayerName, channelName) {
            if (!comp) comp = vac34_AEDom.getActiveComp();
            if (!comp) {
                return { valid: false, state: "NO_COMP", message: "No active composition." };
            }
            var targetName = audioLayerName || vac34_Config.AUDIO_LAYER_NAME;

            // Resolve by index-first when available, else by name. Duplicate
            // display names never silently redirect to the first match.
            var matches = [];
            try {
                if (comp.numLayers !== undefined) {
                    for (var i = 1; i <= comp.numLayers; i++) {
                        var l = comp.layer(i);
                        if (l && l.name === targetName) {
                            matches.push({ index: i, layer: l });
                        }
                    }
                }
            } catch (e) {}

            if (matches.length === 0) {
                return {
                    valid: false,
                    state: "AUDIO_MISSING",
                    layer: null,
                    channel: null,
                    message: "Cannot apply: Audio source missing. Create Audio Amplitude first (Animation > Keyframe Assistant > Convert Audio to Keyframes)."
                };
            }
            if (matches.length > 1) {
                return {
                    valid: false,
                    state: "SOURCE_AMBIGUOUS",
                    layer: null,
                    channel: null,
                    message: "AUDIO_SOURCE_IDENTITY_LOST: multiple layers named '" + targetName + "' found. Audio source identity is ambiguous."
                };
            }

            var lyr = matches[0].layer;
            var effects = lyr.property("ADBE Effect Parade") || lyr.property("Effects");
            if (!effects) {
                return {
                    valid: false,
                    state: "CHANNEL_MISSING",
                    layer: null,
                    channel: null,
                    message: "Cannot apply: Audio layer '" + targetName + "' has no audio channels."
                };
            }

            var chanName = channelName || "Both Channels";
            var chanProp = effects.property(chanName);
            if (!chanProp) {
                return {
                    valid: false,
                    state: "CHANNEL_MISSING",
                    layer: lyr,
                    channel: null,
                    message: "Cannot apply: Audio channel '" + chanName + "' not found on layer '" + targetName + "'."
                };
            }

            return { valid: true, state: "AUDIO_READY", layer: lyr, channel: chanProp, message: "Audio source verified." };
        },

        // Compact status for always-visible UI display: AUDIO READY | AUDIO MISSING |
        // CHANNEL MISSING | SOURCE AMBIGUOUS | NO COMP
        getAudioStatus: function(comp, audioLayerName, channelName) {
            var res = this.validateAudioSource(comp, audioLayerName, channelName);
            if (res.valid) {
                return { state: "AUDIO_READY", valid: true, layerName: audioLayerName || vac34_Config.AUDIO_LAYER_NAME, message: "Audio source verified." };
            }
            return {
                state: res.state || "AUDIO_MISSING",
                valid: false,
                layerName: audioLayerName || vac34_Config.AUDIO_LAYER_NAME,
                message: res.message
            };
        },

        generateAudioLinkCode: function(audioLayerName, channelName) {
            var safeName = audioLayerName || vac34_Config.AUDIO_LAYER_NAME;
            var safeChannel = channelName || "Both Channels";
            var encodedLayer = escapeStringLiteral(safeName);
            var encodedChannel = escapeStringLiteral(safeChannel);

            return [
                '// [vac34: Audio Link]',
                'var _audioLyr = null;',
                'try { _audioLyr = thisComp.layer(' + encodedLayer + '); } catch(e) {}',
                'var _rawAmp = 0;',
                'if (_audioLyr && _audioLyr.effect && _audioLyr.effect(' + encodedChannel + ')) {',
                '    _rawAmp = _audioLyr.effect(' + encodedChannel + ')(1);',
                '} else {',
                '    _rawAmp = 0; // Fallback: no audio layer',
                '}'
            ].join('\n');
        },

        generateTemporalEnvelopeCode: function(audioLayerName, channelName, attackFrames, releaseFrames, threshold) {
            var safeName = audioLayerName || vac34_Config.AUDIO_LAYER_NAME;
            var safeChannel = channelName || "Both Channels";
            var maxLookback = 30; // Bound sampling to 30 frames for guaranteed UI responsiveness
            var encodedLayer = escapeStringLiteral(safeName);
            var encodedChannel = escapeStringLiteral(safeChannel);

            return [
                '// [vac34: Temporal Attack/Release Envelope (Bounded Lookback)]',
                'var _audioLyr = null;',
                'try { _audioLyr = thisComp.layer(' + encodedLayer + '); } catch(e) {}',
                'var _env = 0;',
                'if (_audioLyr && _audioLyr.effect && _audioLyr.effect(' + encodedChannel + ')) {',
                '    var _ampProp = _audioLyr.effect(' + encodedChannel + ')(1);',
                '    var _curTime = time;',
                '    var _fps = 1.0 / thisComp.frameDuration;',
                '    var _lookback = Math.min(' + maxLookback + ', Math.floor(_curTime * _fps));',
                '    var _peak = 0;',
                '    var _th = ' + (threshold || 5) + ';',
                '    for (var _f = 0; _f <= _lookback; _f++) {',
                '        var _tSample = _curTime - (_f * thisComp.frameDuration);',
                '        var _v = _ampProp.valueAtTime(_tSample);',
                '        if (_v >= _th) {',
                '            var _decay = Math.max(0, 1.0 - (_f / ' + (releaseFrames || 12) + '));',
                '            if (_decay > _peak) _peak = _decay;',
                '        }',
                '    }',
                '    _env = _peak;',
                '} else { _env = 0; }'
            ].join('\n');
        }
    };
})();