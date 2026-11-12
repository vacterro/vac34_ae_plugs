// Debug: replicate test_05 mock and print applyRecipe warnings
const fs = require('fs');
const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
new Function('thisObj', bundle)(global);

const thresholdProp = {
    name: "Threshold",
    matchName: "ADBE Starglow-0005",
    propertyIndex: 1,
    propertyValueType: 1,
    canSetExpression: true,
    value: 262.0,
    expression: "",
    parentProperty: null
};

const starglow = {
    name: "Starglow",
    matchName: "STARGLOW",
    propertyIndex: 1,
    numProperties: 1,
    property: (p) => (p === 1 || p === "Threshold") ? thresholdProp : null
};

const effectsGroup = {
    name: "Effects",
    matchName: "ADBE Effect Parade",
    numProperties: 1,
    property: (p) => (p === 1 || p === "Starglow") ? starglow : null,
    addProperty: (m) => {
        let _v = 0;
        return {
            name: m,
            matchName: m,
            property: () => ({
                get value() { return _v; },
                setValue: (v) => { _v = v; }
            }),
            remove: () => {}
        };
    }
};

const lyr = {
    name: "Adjustment Layer 8",
    selectedProperties: [thresholdProp],
    property: (p) => (p === "Effects" || p === "ADBE Effect Parade") ? effectsGroup : null
};
thresholdProp.parentProperty = starglow;
starglow.parentProperty = effectsGroup;
effectsGroup.parentProperty = lyr;

const audioLayer = {
    name: "Audio Amplitude",
    property: (p) => ({
        property: (chan) => ({
            property: () => ({ valueAtTime: () => 15 })
        })
    })
};

const comp = {
    name: "Comp",
    selectedLayers: [lyr],
    selectedProperties: [thresholdProp],
    layer: (n) => (n === "Audio Amplitude" ? audioLayer : null)
};

const mapperRecipe = global.vac34_RecipeRegistry.getRecipeById("audio.property.map.scalar");
const res = global.vac34_Engine.applyRecipe(
    comp, [lyr], mapperRecipe,
    { math_mode: 0, amount: 50, output_min: 0, output_max: 100 },
    false, "Audio Amplitude", "Both Channels", "AUTO"
);
console.log(JSON.stringify(res, null, 2));
// descriptor inspection
const desc = global.vac34_AEDom.capturePropertyDescriptor(lyr, thresholdProp);
console.log("descriptor:", JSON.stringify(desc));
console.log("reacquire:", global.vac34_AEDom.reacquireProperty(lyr, desc) === thresholdProp ? "SAME" : String(global.vac34_AEDom.reacquireProperty(lyr, desc)));
