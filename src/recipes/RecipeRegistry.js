/*
 * vac34_AE — Master Expressions Studio
 * RecipeRegistry: Comprehensive Declarative Recipe Database with 2D/3D & Parameter Wiring
 */

var vac34_RecipeRegistry = (function() {
    var CATEGORIES = [
        "All",
        "AUDIO REACTIVE",
        "SCALE",
        "POSITION",
        "ROTATION",
        "OPACITY AND VISIBILITY",
        "COLOR AND STYLING",
        "LOOPS AND TIME",
        "WIGGLE AND NOISE",
        "PHYSICS AND INERTIA",
        "RIGGING AND SPACE",
        "TEXT AND SHAPES",
        "CAMERA AND LIGHT",
        "UTILITIES"
    ];

    function getParamRef(pName, recipe, isMaster, masterName) {
        var effName = vac34_Config.EFFECT_PREFIX + recipe.displayName + " — " + pName;
        if (isMaster) {
            var mName = masterName || vac34_Config.MASTER_LAYER_NAME;
            return 'thisComp.layer(' + vac34_AudioEngine.escapeStringLiteral(mName) + ').effect(' + vac34_AudioEngine.escapeStringLiteral(effName) + ')(1)';
        }
        return 'effect(' + vac34_AudioEngine.escapeStringLiteral(effName) + ')(1)';
    }

    var RECIPES = [
        // ==========================================
        // 1. AUDIO REACTIVE
        // ==========================================
        {
            id: "audio.property.map.scalar",
            displayName: "Audio Reactive Value Mapper",
            category: "AUDIO REACTIVE",
            description: "Maps audio amplitude to any 1D scalar parameter (Starglow Threshold, Glow Radius, Exposure, Slider, etc.).",
            targetProperties: ["Any.Property"],
            targetDimensions: 1,
            requiresAudio: true,
            compositionMode: "additive",
            parameters: [
                { id: "math_mode", name: "Mode (0:Add, 1:Mul, 2:Abs)", label: "Mode", type: "slider", "default": 0, min: 0, max: 2, unit: "",
                  options: [{ label: "Add", value: 0 }, { label: "Multiply", value: 1 }, { label: "Absolute", value: 2 }] },
                { id: "amount", name: "Amount %", type: "slider", "default": 50, min: -500, max: 500, unit: "%" },
                { id: "output_min", name: "Output Min", type: "slider", "default": 0, min: -1000, max: 1000, unit: "" },
                { id: "output_max", name: "Output Max", type: "slider", "default": 100, min: -1000, max: 1000, unit: "" },
                { id: "audio_threshold", name: "Audio Trigger Threshold", type: "slider", "default": 8, min: 0, max: 100, unit: "" },
                { id: "input_max", name: "Audio Input Max", type: "slider", "default": 30, min: 1, max: 100, unit: "" },
                { id: "smoothing", name: "Smooth Frames", type: "slider", "default": 3, min: 1, max: 10, unit: "f" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var pMode = getParamRef("Mode (0:Add, 1:Mul, 2:Abs)", this, isMaster, masterName);
                var pAmount = getParamRef("Amount %", this, isMaster, masterName);
                var pOutMin = getParamRef("Output Min", this, isMaster, masterName);
                var pOutMax = getParamRef("Output Max", this, isMaster, masterName);
                var pThresh = getParamRef("Audio Trigger Threshold", this, isMaster, masterName);
                var pInMax = getParamRef("Audio Input Max", this, isMaster, masterName);
                var pSmooth = getParamRef("Smooth Frames", this, isMaster, masterName);

                var safeName = audioName || vac34_Config.AUDIO_LAYER_NAME;
                var safeChan = audioChan || "Both Channels";
                var encodedAudio = vac34_AudioEngine.escapeStringLiteral(safeName);
                var encodedChan = vac34_AudioEngine.escapeStringLiteral(safeChan);

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _audioLyr = null;',
                    'try { _audioLyr = thisComp.layer(' + encodedAudio + '); } catch(e) {}',
                    'var _sm = Math.max(1, Math.min(10, Math.floor(' + pSmooth + ')));',
                    'var _rawAmp = 0;',
                    'if (_audioLyr && _audioLyr.effect && _audioLyr.effect(' + encodedChan + ')) {',
                    '    var _prop = _audioLyr.effect(' + encodedChan + ')(1);',
                    '    var _sum = 0;',
                    '    for (var _f = 0; _f < _sm; _f++) {',
                    '        _sum += _prop.valueAtTime(time - (_f * thisComp.frameDuration));',
                    '    }',
                    '    _rawAmp = _sum / _sm;',
                    '}',
                    'var _th = ' + pThresh + ';',
                    'var _inMax = ' + pInMax + ';',
                    'var _max = Math.max(_th + 0.001, _inMax);',
                    'var _norm = 0;',
                    'if (_rawAmp > _th) {',
                    '    _norm = ease(_rawAmp, _th, _max, 0, 1);',
                    '}',
                    'var _amt = ' + pAmount + ' / 100.0;',
                    'var _min = ' + pOutMin + ';',
                    'var _maxOut = ' + pOutMax + ';',
                    'var _m = Math.round(' + pMode + ');',
                    'var _mapped = 0;',
                    'if (_m === 1) {',
                    '    // Multiplicative mode: Output Min and Output Max define factor percentage range',
                    '    var _factor = 1.0 + ((_min + (_maxOut - _min) * _norm) / 100.0) * _amt;',
                    '    value * _factor;',
                    '} else if (_m === 2) {',
                    '    // Absolute mode: blend between value and absolute mapped output',
                    '    var _absMapped = _min + (_maxOut - _min) * _norm;',
                    '    value + (_absMapped - value) * _amt;',
                    '} else {',
                    '    // Additive mode: add scaled offset range',
                    '    _mapped = (_min + (_maxOut - _min) * _norm) * _amt;',
                    '    value + _mapped;',
                    '}'
                ].join('\n');
            }
        },
        {
            id: "audio.scale.pump",
            displayName: "Beat Scale Pump",
            category: "AUDIO REACTIVE",
            description: "Pumps layer scale rhythmically to audio amplitude peaks while preserving base scale.",
            targetProperties: ["Transform.Scale"],
            targetDimensions: 2,
            requiresAudio: true,
            compositionMode: "multiplicative",
            parameters: [
                { id: "intensity", name: "Intensity %", type: "slider", "default": 35, min: 0, max: 200, unit: "%" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 8, min: 0, max: 100, unit: "" },
                { id: "input_max", name: "Audio Max", type: "slider", "default": 30, min: 5, max: 100, unit: "" },
                { id: "smoothing", name: "Smooth Frames", type: "slider", "default": 3, min: 1, max: 10, unit: "f" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pIntensity = getParamRef("Intensity %", this, isMaster, masterName);
                var pThreshold = getParamRef("Threshold", this, isMaster, masterName);
                var pInputMax = getParamRef("Audio Max", this, isMaster, masterName);
                var pSmooth = getParamRef("Smooth Frames", this, isMaster, masterName);
                var safeName = audioName || vac34_Config.AUDIO_LAYER_NAME;
                var safeChan = audioChan || "Both Channels";

                var scaleReturn = is3D ? '[value[0] * _factor, value[1] * _factor, value[2] * _factor];' : '[value[0] * _factor, value[1] * _factor];';

                var encodedAudio = vac34_AudioEngine.escapeStringLiteral(safeName);
                var encodedChan = vac34_AudioEngine.escapeStringLiteral(safeChan);

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _audioLyr = null;',
                    'try { _audioLyr = thisComp.layer(' + encodedAudio + '); } catch(e) {}',
                    'var _sm = Math.max(1, Math.min(10, Math.floor(' + pSmooth + ')));',
                    'var _rawAmp = 0;',
                    'if (_audioLyr && _audioLyr.effect && _audioLyr.effect(' + encodedChan + ')) {',
                    '    var _prop = _audioLyr.effect(' + encodedChan + ')(1);',
                    '    var _sum = 0;',
                    '    for (var _f = 0; _f < _sm; _f++) {',
                    '        _sum += _prop.valueAtTime(time - (_f * thisComp.frameDuration));',
                    '    }',
                    '    _rawAmp = _sum / _sm;',
                    '}',
                    'var _intensity = ' + pIntensity + ' / 100.0;',
                    'var _th = ' + pThreshold + ';',
                    'var _max = Math.max(_th + 1, ' + pInputMax + ');',
                    'var _boost = 0;',
                    'if (_rawAmp > _th) {',
                    '    _boost = ease(_rawAmp, _th, _max, 0, _intensity);',
                    '}',
                    'var _factor = 1.0 + _boost;',
                    scaleReturn
                ].join('\n');
            }
        },
        {
            id: "audio.position.jump",
            displayName: "Audio Vertical Jump",
            category: "AUDIO REACTIVE",
            description: "Launches the layer vertically on audio beats with spring return.",
            targetProperties: ["Transform.Position"],
            targetDimensions: 2,
            requiresAudio: true,
            compositionMode: "additive",
            parameters: [
                { id: "jump_height", name: "Jump Height", type: "slider", "default": 80, min: 0, max: 500, unit: "px" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 10, min: 0, max: 100, unit: "" },
                { id: "input_max", name: "Audio Max", type: "slider", "default": 35, min: 5, max: 100, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var aRef = vac34_AudioEngine.generateAudioLinkCode(audioName, audioChan);
                var pHeight = getParamRef("Jump Height", this, isMaster, masterName);
                var pTh = getParamRef("Threshold", this, isMaster, masterName);
                var pMax = getParamRef("Audio Max", this, isMaster, masterName);

                var posReturn = is3D ? '[value[0], value[1] + _dy, value[2]];' : '[value[0], value[1] + _dy];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    aRef,
                    'var _h = ' + pHeight + ';',
                    'var _th = ' + pTh + ';',
                    'var _max = Math.max(_th + 1, ' + pMax + ');',
                    'var _dy = 0;',
                    'if (_rawAmp > _th) {',
                    '    _dy = ease(_rawAmp, _th, _max, 0, -_h);',
                    '}',
                    posReturn
                ].join('\n');
            }
        },
        {
            id: "audio.position.shake",
            displayName: "Audio Reactive Shake",
            category: "AUDIO REACTIVE",
            description: "Modulates position shake intensity dynamically with music amplitude.",
            targetProperties: ["Transform.Position"],
            targetDimensions: 2,
            requiresAudio: true,
            compositionMode: "additive",
            parameters: [
                { id: "freq", name: "Shake Frequency", type: "slider", "default": 18, min: 1, max: 60, unit: "Hz" },
                { id: "max_amt", name: "Max Amount", type: "slider", "default": 40, min: 0, max: 200, unit: "px" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 6, min: 0, max: 100, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var aRef = vac34_AudioEngine.generateAudioLinkCode(audioName, audioChan);
                var pFreq = getParamRef("Shake Frequency", this, isMaster, masterName);
                var pAmt = getParamRef("Max Amount", this, isMaster, masterName);
                var pTh = getParamRef("Threshold", this, isMaster, masterName);

                var shakeReturn = is3D ? '[value[0] + (_w[0] - value[0]), value[1] + (_w[1] - value[1]), value[2]];' : '[value[0] + (_w[0] - value[0]), value[1] + (_w[1] - value[1])];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    aRef,
                    'var _f = ' + pFreq + ';',
                    'var _maxAmt = ' + pAmt + ';',
                    'var _th = ' + pTh + ';',
                    'var _curAmt = 0;',
                    'if (_rawAmp > _th) {',
                    '    _curAmt = ease(_rawAmp, _th, _th + 25, 0, _maxAmt);',
                    '}',
                    'if (_curAmt > 0) {',
                    '    var _w = wiggle(_f, _curAmt);',
                    '    ' + shakeReturn,
                    '} else {',
                    '    value;',
                    '}'
                ].join('\n');
            }
        },
        {
            id: "audio.rotation.wobble",
            displayName: "Audio Rotation Wobble",
            category: "AUDIO REACTIVE",
            description: "Twists layer rotation back and forth reacting to audio amplitude.",
            targetProperties: ["Transform.Rotation"],
            targetDimensions: 1,
            requiresAudio: true,
            compositionMode: "additive",
            parameters: [
                { id: "max_angle", name: "Max Angle", type: "angle", "default": 15, min: 0, max: 180, unit: "°" },
                { id: "speed", name: "Oscillation Speed", type: "slider", "default": 12, min: 1, max: 50, unit: "Hz" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 5, min: 0, max: 100, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var aRef = vac34_AudioEngine.generateAudioLinkCode(audioName, audioChan);
                var pAngle = getParamRef("Max Angle", this, isMaster, masterName);
                var pSpeed = getParamRef("Oscillation Speed", this, isMaster, masterName);
                var pTh = getParamRef("Threshold", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    aRef,
                    'var _maxAngle = ' + pAngle + ';',
                    'var _speed = ' + pSpeed + ';',
                    'var _th = ' + pTh + ';',
                    'var _intensity = 0;',
                    'if (_rawAmp > _th) {',
                    '    _intensity = ease(_rawAmp, _th, _th + 30, 0, _maxAngle);',
                    '}',
                    'var _rot = Math.sin(time * _speed * Math.PI * 2) * _intensity;',
                    'value + _rot;'
                ].join('\n');
            }
        },
        {
            id: "audio.opacity.flash",
            displayName: "Audio Flash Strobe",
            category: "AUDIO REACTIVE",
            description: "Strobes layer opacity on beat peaks above a threshold.",
            targetProperties: ["Transform.Opacity"],
            targetDimensions: 1,
            requiresAudio: true,
            compositionMode: "replace",
            parameters: [
                { id: "min_opacity", name: "Base Opacity", type: "slider", "default": 20, min: 0, max: 100, unit: "%" },
                { id: "max_opacity", name: "Peak Opacity", type: "slider", "default": 100, min: 0, max: 100, unit: "%" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 12, min: 0, max: 100, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var aRef = vac34_AudioEngine.generateAudioLinkCode(audioName, audioChan);
                var pMin = getParamRef("Base Opacity", this, isMaster, masterName);
                var pMax = getParamRef("Peak Opacity", this, isMaster, masterName);
                var pTh = getParamRef("Threshold", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    aRef,
                    'var _min = ' + pMin + ';',
                    'var _max = ' + pMax + ';',
                    'var _th = ' + pTh + ';',
                    'if (_rawAmp >= _th) {',
                    '    ease(_rawAmp, _th, _th + 20, _min, _max);',
                    '} else {',
                    '    _min;',
                    '}'
                ].join('\n');
            }
        },
        {
            id: "audio.envelope.attack_release",
            displayName: "Audio Attack/Release Envelope",
            category: "AUDIO REACTIVE",
            description: "True temporal peak envelope follower with smooth release decay.",
            targetProperties: ["Transform.Scale", "Slider"],
            targetDimensions: 1,
            requiresAudio: true,
            compositionMode: "multiplicative",
            parameters: [
                { id: "release_frames", name: "Release Frames", type: "slider", "default": 12, min: 2, max: 30, unit: "f" },
                { id: "threshold", name: "Threshold", type: "slider", "default": 8, min: 0, max: 100, unit: "" },
                { id: "boost", name: "Boost Amount", type: "slider", "default": 40, min: 0, max: 200, unit: "%" }
            ],
            generateExpression: function(layer, isMaster, masterName, pVals, audioName, audioChan) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pRel = getParamRef("Release Frames", this, isMaster, masterName);
                var pTh = getParamRef("Threshold", this, isMaster, masterName);
                var pBoost = getParamRef("Boost Amount", this, isMaster, masterName);
                var safeName = audioName || vac34_Config.AUDIO_LAYER_NAME;
                var safeChan = audioChan || "Both Channels";

                var scaleReturn = is3D ? '[value[0] * _s, value[1] * _s, value[2] * _s];' : '[value[0] * _s, value[1] * _s];';

                var encodedAudio = vac34_AudioEngine.escapeStringLiteral(safeName);
                var encodedChan = vac34_AudioEngine.escapeStringLiteral(safeChan);

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _audioLyr = null;',
                    'try { _audioLyr = thisComp.layer(' + encodedAudio + '); } catch(e) {}',
                    'var _env = 0;',
                    'var _relFrames = Math.max(1, ' + pRel + ');',
                    'var _th = ' + pTh + ';',
                    'var _boost = ' + pBoost + ' / 100.0;',
                    'if (_audioLyr && _audioLyr.effect && _audioLyr.effect(' + encodedChan + ')) {',
                    '    var _ampProp = _audioLyr.effect(' + encodedChan + ')(1);',
                    '    var _curTime = time;',
                    '    var _fps = 1.0 / thisComp.frameDuration;',
                    '    var _lookback = Math.min(30, Math.floor(_curTime * _fps));',
                    '    var _peak = 0;',
                    '    for (var _f = 0; _f <= _lookback; _f++) {',
                    '        var _tSample = _curTime - (_f * thisComp.frameDuration);',
                    '        var _v = _ampProp.valueAtTime(_tSample);',
                    '        if (_v >= _th) {',
                    '            var _decay = Math.max(0, 1.0 - (_f / _relFrames));',
                    '            if (_decay > _peak) _peak = _decay;',
                    '        }',
                    '    }',
                    '    _env = _peak;',
                    '}',
                    'var _s = 1.0 + (_env * _boost);',
                    scaleReturn
                ].join('\n');
            }
        },

        // ==========================================
        // 2. SCALE
        // ==========================================
        {
            id: "scale.uniform.breathing",
            displayName: "Sine Breathing Scale",
            category: "SCALE",
            description: "Smooth organic breathing oscillation around base scale.",
            targetProperties: ["Transform.Scale"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "multiplicative",
            parameters: [
                { id: "freq", name: "Frequency (Hz)", type: "slider", "default": 0.8, min: 0.1, max: 10, unit: "Hz" },
                { id: "amount", name: "Amount %", type: "slider", "default": 12, min: 0, max: 100, unit: "%" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pFreq = getParamRef("Frequency (Hz)", this, isMaster, masterName);
                var pAmt = getParamRef("Amount %", this, isMaster, masterName);
                var scaleReturn = is3D ? '[value[0] * _s, value[1] * _s, value[2] * _s];' : '[value[0] * _s, value[1] * _s];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _f = ' + pFreq + ';',
                    'var _amt = ' + pAmt + ' / 100.0;',
                    'var _wave = Math.sin(time * _f * Math.PI * 2) * _amt;',
                    'var _s = 1.0 + _wave;',
                    scaleReturn
                ].join('\n');
            }
        },
        {
            id: "scale.squash.stretch",
            displayName: "Squash & Stretch",
            category: "SCALE",
            description: "Maintains perceptual volume while oscillating X and Y in opposite phases.",
            targetProperties: ["Transform.Scale"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "multiplicative",
            parameters: [
                { id: "freq", name: "Frequency (Hz)", type: "slider", "default": 1.5, min: 0.1, max: 15, unit: "Hz" },
                { id: "amount", name: "Squash %", type: "slider", "default": 20, min: 0, max: 80, unit: "%" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pFreq = getParamRef("Frequency (Hz)", this, isMaster, masterName);
                var pAmt = getParamRef("Squash %", this, isMaster, masterName);
                var scaleReturn = is3D ? '[value[0] * _sx, value[1] * _sy, value[2]];' : '[value[0] * _sx, value[1] * _sy];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _f = ' + pFreq + ';',
                    'var _amt = ' + pAmt + ' / 100.0;',
                    'var _wave = Math.sin(time * _f * Math.PI * 2) * _amt;',
                    'var _sx = 1.0 + _wave;',
                    'var _sy = 1.0 / _sx; // Preserves 2D area',
                    scaleReturn
                ].join('\n');
            }
        },
        {
            id: "scale.pulse.heartbeat",
            displayName: "Double Pulse Heartbeat",
            category: "SCALE",
            description: "Classic lub-dub anatomical heartbeat pulse.",
            targetProperties: ["Transform.Scale"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "multiplicative",
            parameters: [
                { id: "bpm", name: "Heart BPM", type: "slider", "default": 72, min: 30, max: 200, unit: "BPM" },
                { id: "pump", name: "Pump %", type: "slider", "default": 25, min: 0, max: 100, unit: "%" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pBpm = getParamRef("Heart BPM", this, isMaster, masterName);
                var pPump = getParamRef("Pump %", this, isMaster, masterName);
                var scaleReturn = is3D ? '[value[0] * _s, value[1] * _s, value[2] * _s];' : '[value[0] * _s, value[1] * _s];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _bpm = ' + pBpm + ';',
                    'var _pump = ' + pPump + ' / 100.0;',
                    'var _cycle = (time * (_bpm / 60.0)) % 1.0;',
                    'var _boost = 0;',
                    'if (_cycle < 0.15) {',
                    '    _boost = Math.sin((_cycle / 0.15) * Math.PI) * _pump;',
                    '} else if (_cycle >= 0.25 && _cycle < 0.40) {',
                    '    _boost = Math.sin(((_cycle - 0.25) / 0.15) * Math.PI) * (_pump * 0.6);',
                    '}',
                    'var _s = 1.0 + _boost;',
                    scaleReturn
                ].join('\n');
            }
        },

        // ==========================================
        // 3. POSITION
        // ==========================================
        {
            id: "position.wiggle.smooth",
            displayName: "Smooth 2D Wiggle",
            category: "POSITION",
            description: "Independent X and Y wiggle sliders for precise organic drift.",
            targetProperties: ["Transform.Position"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "additive",
            parameters: [
                { id: "freq", name: "Frequency (Hz)", type: "slider", "default": 2.0, min: 0.1, max: 30, unit: "Hz" },
                { id: "amt_x", name: "Amount X", type: "slider", "default": 30, min: 0, max: 500, unit: "px" },
                { id: "amt_y", name: "Amount Y", type: "slider", "default": 30, min: 0, max: 500, unit: "px" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pFreq = getParamRef("Frequency (Hz)", this, isMaster, masterName);
                var pX = getParamRef("Amount X", this, isMaster, masterName);
                var pY = getParamRef("Amount Y", this, isMaster, masterName);
                var posReturn = is3D ? '[value[0] + (_wx[0] - value[0]), value[1] + (_wy[1] - value[1]), value[2]];' : '[value[0] + (_wx[0] - value[0]), value[1] + (_wy[1] - value[1])];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _f = ' + pFreq + ';',
                    'var _ax = ' + pX + ';',
                    'var _ay = ' + pY + ';',
                    'var _wx = wiggle(_f, _ax);',
                    'var _wy = wiggle(_f, _ay);',
                    posReturn
                ].join('\n');
            }
        },
        {
            id: "position.orbit.circular",
            displayName: "Circular Orbit",
            category: "POSITION",
            description: "Rotates position smoothly in a 2D orbit around its base anchor point.",
            targetProperties: ["Transform.Position"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "additive",
            parameters: [
                { id: "radius", name: "Radius", type: "slider", "default": 120, min: 0, max: 1000, unit: "px" },
                { id: "speed", name: "Speed (rev/s)", type: "slider", "default": 0.5, min: -10, max: 10, unit: "rps" },
                { id: "phase", name: "Phase Offset", type: "angle", "default": 0, min: 0, max: 360, unit: "°" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pRad = getParamRef("Radius", this, isMaster, masterName);
                var pSpd = getParamRef("Speed (rev/s)", this, isMaster, masterName);
                var pPh = getParamRef("Phase Offset", this, isMaster, masterName);
                var posReturn = is3D ? '[value[0] + (Math.cos(_ang) * _r), value[1] + (Math.sin(_ang) * _r), value[2]];' : '[value[0] + (Math.cos(_ang) * _r), value[1] + (Math.sin(_ang) * _r)];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _r = ' + pRad + ';',
                    'var _spd = ' + pSpd + ';',
                    'var _phaseRad = (' + pPh + ') * (Math.PI / 180.0);',
                    'var _ang = (time * _spd * Math.PI * 2) + _phaseRad;',
                    posReturn
                ].join('\n');
            }
        },
        {
            id: "position.drift.linear",
            displayName: "Continuous Directional Drift",
            category: "POSITION",
            description: "Constant directional floating motion in pixels per second.",
            targetProperties: ["Transform.Position"],
            targetDimensions: 2,
            requiresAudio: false,
            compositionMode: "additive",
            parameters: [
                { id: "speed_x", name: "Speed X", type: "slider", "default": 25, min: -500, max: 500, unit: "px/s" },
                { id: "speed_y", name: "Speed Y", type: "slider", "default": -15, min: -500, max: 500, unit: "px/s" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var is3D = vac34_AEDom.isLayer3D(layer);
                var pX = getParamRef("Speed X", this, isMaster, masterName);
                var pY = getParamRef("Speed Y", this, isMaster, masterName);
                var posReturn = is3D ? '[value[0] + (time * _vx), value[1] + (time * _vy), value[2]];' : '[value[0] + (time * _vx), value[1] + (time * _vy)];';

                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _vx = ' + pX + ';',
                    'var _vy = ' + pY + ';',
                    posReturn
                ].join('\n');
            }
        },

        // ==========================================
        // 4. ROTATION
        // ==========================================
        {
            id: "rotation.spin.continuous",
            displayName: "Continuous Spin",
            category: "ROTATION",
            description: "Spins layer endlessly at a specified rotational velocity.",
            targetProperties: ["Transform.Rotation"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "additive",
            parameters: [
                { id: "speed", name: "Speed (°/s)", type: "slider", "default": 45, min: -720, max: 720, unit: "°/s" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pSpd = getParamRef("Speed (°/s)", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _spd = ' + pSpd + ';',
                    'value + (time * _spd);'
                ].join('\n');
            }
        },
        {
            id: "rotation.pendulum.swing",
            displayName: "Pendulum Swing",
            category: "ROTATION",
            description: "Simulates harmonic pendulum oscillation with amplitude and frequency.",
            targetProperties: ["Transform.Rotation"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "additive",
            parameters: [
                { id: "amplitude", name: "Swing Angle", type: "angle", "default": 30, min: 0, max: 180, unit: "°" },
                { id: "freq", name: "Frequency (Hz)", type: "slider", "default": 0.8, min: 0.1, max: 10, unit: "Hz" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pAmp = getParamRef("Swing Angle", this, isMaster, masterName);
                var pFreq = getParamRef("Frequency (Hz)", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _amp = ' + pAmp + ';',
                    'var _f = ' + pFreq + ';',
                    'value + (Math.sin(time * _f * Math.PI * 2) * _amp);'
                ].join('\n');
            }
        },

        // ==========================================
        // 5. OPACITY AND VISIBILITY
        // ==========================================
        {
            id: "opacity.pulse.sine",
            displayName: "Sine Opacity Pulse",
            category: "OPACITY AND VISIBILITY",
            description: "Smooth pulsing transparency between min and max bounds.",
            targetProperties: ["Transform.Opacity"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "min_op", name: "Min Opacity", type: "slider", "default": 20, min: 0, max: 100, unit: "%" },
                { id: "max_op", name: "Max Opacity", type: "slider", "default": 100, min: 0, max: 100, unit: "%" },
                { id: "speed", name: "Rate (Hz)", type: "slider", "default": 1.0, min: 0.1, max: 15, unit: "Hz" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pMin = getParamRef("Min Opacity", this, isMaster, masterName);
                var pMax = getParamRef("Max Opacity", this, isMaster, masterName);
                var pSpd = getParamRef("Rate (Hz)", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _min = ' + pMin + ';',
                    'var _max = ' + pMax + ';',
                    'var _rate = ' + pSpd + ';',
                    'var _sin = (Math.sin(time * _rate * Math.PI * 2) + 1.0) / 2.0;',
                    'linear(_sin, 0, 1, _min, _max);'
                ].join('\n');
            }
        },
        {
            id: "opacity.blink.strobe",
            displayName: "Strobe Blink",
            category: "OPACITY AND VISIBILITY",
            description: "Hard digital on/off strobe with customizable duty cycle.",
            targetProperties: ["Transform.Opacity"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "freq", name: "Strobe Freq", type: "slider", "default": 4, min: 0.5, max: 30, unit: "Hz" },
                { id: "duty", name: "Duty Cycle %", type: "slider", "default": 50, min: 5, max: 95, unit: "%" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pFreq = getParamRef("Strobe Freq", this, isMaster, masterName);
                var pDuty = getParamRef("Duty Cycle %", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _f = ' + pFreq + ';',
                    'var _duty = ' + pDuty + ' / 100.0;',
                    'var _phase = (time * _f) % 1.0;',
                    '(_phase < _duty) ? 100 : 0;'
                ].join('\n');
            }
        },

        // ==========================================
        // 6. LOOPS AND TIME
        // ==========================================
        {
            id: "loops.cycle.keyframes",
            displayName: "Loop Out Cycle",
            category: "LOOPS AND TIME",
            description: "Repeats all animated keyframes in an infinite cycle.",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "num_keyframes", name: "Num Keyframes", type: "slider", "default": 0, min: 0, max: 20, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pK = getParamRef("Num Keyframes", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _k = Math.floor(' + pK + ');',
                    'if (numKeys > 1) {',
                    '    loopOut("cycle", _k);',
                    '} else {',
                    '    value;',
                    '}'
                ].join('\n');
            }
        },
        {
            id: "loops.pingpong.keyframes",
            displayName: "Loop Out Ping-Pong",
            category: "LOOPS AND TIME",
            description: "Bounces keyframed animation back and forth continuously.",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [],
            generateExpression: function() {
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'if (numKeys > 1) {',
                    '    loopOut("pingpong");',
                    '} else {',
                    '    value;',
                    '}'
                ].join('\n');
            }
        },
        {
            id: "loops.time.posterize",
            displayName: "Posterize Time (Stop Motion)",
            category: "LOOPS AND TIME",
            description: "Steps motion at a retro lower framerate (e.g. 12 fps stop motion).",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "fps", name: "Target FPS", type: "slider", "default": 12, min: 1, max: 60, unit: "fps" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pFps = getParamRef("Target FPS", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'posterizeTime(' + pFps + ');',
                    'value;'
                ].join('\n');
            }
        },

        // ==========================================
        // 7. WIGGLE AND NOISE
        // ==========================================
        {
            id: "wiggle.noise.controlled",
            displayName: "Master Controlled Wiggle",
            category: "WIGGLE AND NOISE",
            description: "Full-featured wiggle with frequency, amount, and octave controls.",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "freq", name: "Frequency (Hz)", type: "slider", "default": 3.0, min: 0.1, max: 30, unit: "Hz" },
                { id: "amt", name: "Amount", type: "slider", "default": 50, min: 0, max: 1000, unit: "" },
                { id: "octaves", name: "Octaves Detail", type: "slider", "default": 1, min: 1, max: 4, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pFreq = getParamRef("Frequency (Hz)", this, isMaster, masterName);
                var pAmt = getParamRef("Amount", this, isMaster, masterName);
                var pOct = getParamRef("Octaves Detail", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _f = ' + pFreq + ';',
                    'var _a = ' + pAmt + ';',
                    'var _oct = Math.max(1, Math.floor(' + pOct + '));',
                    'wiggle(_f, _a, _oct);'
                ].join('\n');
            }
        },

        // ==========================================
        // 8. PHYSICS AND INERTIA
        // ==========================================
        {
            id: "physics.spring.inertia",
            displayName: "Inertial Keyframe Bounce",
            category: "PHYSICS AND INERTIA",
            description: "Adds elastic physical overshoot to any keyframed animation.",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "amp", name: "Bounce Amp", type: "slider", "default": 0.08, min: 0.01, max: 0.3, unit: "" },
                { id: "freq", name: "Bounce Freq", type: "slider", "default": 3.5, min: 1.0, max: 15.0, unit: "Hz" },
                { id: "decay", name: "Decay Damping", type: "slider", "default": 5.0, min: 1.0, max: 20.0, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pAmp = getParamRef("Bounce Amp", this, isMaster, masterName);
                var pFreq = getParamRef("Bounce Freq", this, isMaster, masterName);
                var pDec = getParamRef("Decay Damping", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _amp = ' + pAmp + ';',
                    'var _freq = ' + pFreq + ';',
                    'var _decay = ' + pDec + ';',
                    'var _n = 0;',
                    'if (numKeys > 0) {',
                    '    _n = nearestKey(time).index;',
                    '    if (key(_n).time > time) _n--;',
                    '}',
                    'if (_n > 0) {',
                    '    var _t = time - key(_n).time;',
                    '    if (_t > 0 && _t < 2.0) {',
                    '        var _v = velocityAtTime(key(_n).time - 0.001);',
                    '        var _k = (_amp * Math.sin(_freq * _t * 2 * Math.PI) / Math.exp(_decay * _t));',
                    '        if (value instanceof Array) {',
                    '            var _res = [];',
                    '            for (var _i = 0; _i < value.length; _i++) {',
                    '                _res.push(value[_i] + (_v[_i] * _k));',
                    '            }',
                    '            _res;',
                    '        } else {',
                    '            value + (_v * _k);',
                    '        }',
                    '    } else {',
                    '        value;',
                    '    }',
                    '} else {',
                    '    value;',
                    '}'
                ].join('\n');
            }
        },

        // ==========================================
        // 9. RIGGING AND SPACE
        // ==========================================
        {
            id: "rig.crowd.stagger_offset",
            displayName: "Multi-Layer Index Cascade",
            category: "RIGGING AND SPACE",
            description: "Delays property animation based on layer stacking order (index offset).",
            targetProperties: ["Any.Property"],
            targetDimensions: 0,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "delay_sec", name: "Delay per Layer", type: "slider", "default": 0.08, min: 0.01, max: 1.0, unit: "s" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pDelay = getParamRef("Delay per Layer", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _dt = ' + pDelay + ';',
                    'var _delay = (index - 1) * _dt;',
                    'valueAtTime(time - _delay);'
                ].join('\n');
            }
        },

        // ==========================================
        // 10. TEXT AND SHAPES
        // ==========================================
        {
            id: "text.counter.numeric",
            displayName: "Animated Number Counter",
            category: "TEXT AND SHAPES",
            description: "Converts animated slider or keyframes into clean rounded text display.",
            targetProperties: ["Text.SourceText"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "decimals", name: "Decimals", type: "slider", "default": 0, min: 0, max: 4, unit: "" },
                { id: "val", name: "Counter Value", type: "slider", "default": 100, min: 0, max: 100000, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pDec = getParamRef("Decimals", this, isMaster, masterName);
                var pVal = getParamRef("Counter Value", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _val = ' + pVal + ';',
                    'var _dec = Math.max(0, Math.floor(' + pDec + '));',
                    '_val.toFixed(_dec);'
                ].join('\n');
            }
        },

        // ==========================================
        // 11. UTILITIES
        // ==========================================
        {
            id: "util.math.clamp",
            displayName: "Safe Value Clamp",
            category: "UTILITIES",
            description: "Restricts property value within minimum and maximum limits.",
            targetProperties: ["Any.Property"],
            targetDimensions: 1,
            requiresAudio: false,
            compositionMode: "replace",
            parameters: [
                { id: "min_val", name: "Min Value", type: "slider", "default": 0, min: -1000, max: 1000, unit: "" },
                { id: "max_val", name: "Max Value", type: "slider", "default": 100, min: -1000, max: 1000, unit: "" }
            ],
            generateExpression: function(layer, isMaster, masterName) {
                var pMin = getParamRef("Min Value", this, isMaster, masterName);
                var pMax = getParamRef("Max Value", this, isMaster, masterName);
                return [
                    vac34_Config.TAG_PREFIX + this.id + vac34_Config.TAG_SUFFIX,
                    'var _min = ' + pMin + ';',
                    'var _max = ' + pMax + ';',
                    'clamp(value, _min, _max);'
                ].join('\n');
            }
        }
    ];

    return {
        getCategories: function() {
            return CATEGORIES;
        },

        getAllRecipes: function() {
            return RECIPES;
        },

        getRecipeById: function(id) {
            for (var i = 0; i < RECIPES.length; i++) {
                if (RECIPES[i].id === id) return RECIPES[i];
            }
            return null;
        },

        filterRecipes: function(category, query) {
            var filtered = [];
            var q = (query || "").toLowerCase();
            for (var i = 0; i < RECIPES.length; i++) {
                var r = RECIPES[i];
                if (category && category !== "All" && r.category !== category) {
                    continue;
                }
                if (q !== "") {
                    var matchName = r.displayName.toLowerCase().indexOf(q) !== -1;
                    var matchDesc = r.description.toLowerCase().indexOf(q) !== -1;
                    var matchCat = r.category.toLowerCase().indexOf(q) !== -1;
                    if (!matchName && !matchDesc && !matchCat) continue;
                }
                filtered.push(r);
            }
            return filtered;
        }
    };
})();
