const fs = require('fs');
const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
new Function('thisObj', bundle)(global);

const prop = {
    name: "Opacity", propertyValueType: 1, canSetExpression: true,
    _expr: "/* [vac34_AE:scale.uniform.breathing] */\nPREVIOUS_GOOD",
    expressionError: "After Effects error: Invalid expression.",
    expressionEnabled: true, parentProperty: null,
    get expression() { return this._expr; },
    set expression(v) { this._expr = v; }
};
const lyr = { name: "Layer", selectedProperties: [prop], property: (p) => null };
prop.parentProperty = lyr;
const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

const recipe = global.vac34_RecipeRegistry.getRecipeById("scale.uniform.breathing");
const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
console.log(JSON.stringify(res, null, 2));
console.log("prop.expression:", prop.expression);
