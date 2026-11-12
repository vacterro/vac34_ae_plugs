/*
 * vac34_AE — Master Expressions Studio
 * Config & Product Constants
 */

var vac34_Config = {
    PRODUCT_NAME: "vac34_AE",
    PRODUCT_TITLE: "vac34_AE — Master Expressions Studio",
    VERSION: "0.0.1",
    // Source default only. The build pipeline overwrites this with the
    // automatic fingerprint (version + source revision digest) that also lands
    // in release/build_manifest.json, so a stale literal can never pass for a
    // real build.
    BUILD_ID: "20261107.02",
    EFFECT_PREFIX: "vac34 — ",
    TAG_PREFIX: "/* [vac34_AE:",
    TAG_SUFFIX: "] */",
    MASTER_LAYER_NAME: "vac34_Master_Controls",
    AUDIO_LAYER_NAME: "Audio Amplitude",
    PRESET_DIR_NAME: "vac34_AE/presets",
    DEBUG_MODE: false
};
