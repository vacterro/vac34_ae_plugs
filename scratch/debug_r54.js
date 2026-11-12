const fs = require('fs');
const bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
new Function('thisObj', bundle)(global);

const prop = {
    name: "Opacity",
    propertyValueType: 1,
    canSetExpression: true,
    _expr: "/* [vac34_AE:opacity.pulse.sine] */\nPREVIOUS_GOOD",
    get expression() { return this._expr; },
    set expression(v) { this._expr = v; },
    expressionEnabled: true,
    parentProperty: null
};
const lyr = { name: "Solid 1", selectedProperties: [prop], property: () => null };
prop.parentProperty = lyr;
const comp = { name: "Comp", selectedLayers: [lyr], selectedProperties: [prop] };

const recipe = global.vac34_RecipeRegistry.getRecipeById("opacity.pulse.sine");
console.log("recipe:", !!recipe, recipe ? recipe.targetDimensions : null);
recipe.generateExpression = function() { throw new Error("expressionError: bad math"); };

const res = global.vac34_Engine.applyRecipe(comp, [lyr], recipe, {}, false, null, null, "AUTO");
console.log(JSON.stringify(res, null, 2));
console.log("prop.expression:", prop.expression);
