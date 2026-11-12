/*
 * vac34_AE — Master Expressions Studio
 * PresetManager: Pure-JS Recursive Descent JSON Parser, Safe Serializer & Strict Schema Validator
 * ZERO eval / ZERO Function execution.
 */

var vac34_PresetManager = (function() {
    var MAX_INPUT_LENGTH = 262144; // 256 KB max preset file size
    var MAX_DEPTH = 64;            // Prevent recursion stack overflow

    function getPresetFolder() {
        var userDataPath = (typeof Folder !== "undefined" && Folder.userData) ? Folder.userData.fsName : ".";
        var folder = new Folder(userDataPath + "/" + vac34_Config.PRESET_DIR_NAME);
        if (!folder.exists) {
            folder.create();
        }
        return folder;
    }

    // Pure JavaScript Safe JSON Serializer (for ExtendScript environments lacking native JSON.stringify)
    function serializeJSON(value) {
        if (value === null) return "null";
        var t = typeof value;
        if (t === "boolean") return value ? "true" : "false";
        if (t === "number") {
            return isFinite(value) ? String(value) : "null";
        }
        if (t === "string") {
            return '"' + value.replace(/\\/g, '\\\\')
                              .replace(/"/g, '\\"')
                              .replace(/\n/g, '\\n')
                              .replace(/\r/g, '\\r')
                              .replace(/\t/g, '\\t')
                              .replace(/\f/g, '\\f')
                              .replace(/\x08/g, '\\b')
                              .replace(/[\x00-\x1f]/g, function(c) {
                                  var hex = c.charCodeAt(0).toString(16);
                                  return '\\u' + ('0000' + hex).slice(-4);
                              }) + '"';
        }
        if (t === "object") {
            if (value instanceof Array) {
                var elems = [];
                for (var i = 0; i < value.length; i++) {
                    elems.push(serializeJSON(value[i]));
                }
                return "[" + elems.join(",") + "]";
            }
            var pairs = [];
            for (var key in value) {
                if (Object.prototype.hasOwnProperty.call(value, key)) {
                    if (key === "__proto__" || key === "constructor" || key === "prototype") continue;
                    var valStr = serializeJSON(value[key]);
                    if (valStr !== undefined) {
                        pairs.push(serializeJSON(String(key)) + ":" + valStr);
                    }
                }
            }
            return "{" + pairs.join(",") + "}";
        }
        return "null";
    }

    // Pure JavaScript Strict Recursive Descent JSON Parser (Zero eval, Zero Function)
    function parseJSONStrict(source) {
        if (typeof source !== "string") {
            throw new Error("JSON Parse Error: source must be a string");
        }
        if (source.length > MAX_INPUT_LENGTH) {
            throw new Error("JSON Parse Error: input exceeds maximum allowed size (" + MAX_INPUT_LENGTH + " bytes)");
        }

        var at = 0;
        var ch = ' ';
        var depth = 0;

        function error(m) {
            throw new Error("JSON Parse Error: " + m + " at position " + at);
        }

        function next(c) {
            if (c && c !== ch) {
                error("Expected '" + c + "' instead of '" + ch + "'");
            }
            ch = source.charAt(at);
            at += 1;
            return ch;
        }

        function white() {
            while (ch && (ch === ' ' || ch === '\t' || ch === '\n' || ch === '\r')) {
                next();
            }
        }

        function parseString() {
            var s = '';
            if (ch === '"') {
                while (next()) {
                    if (ch === '"') {
                        next();
                        return s;
                    }
                    if (ch < ' ') {
                        error("Unescaped control character in string (0x" + ch.charCodeAt(0).toString(16) + ")");
                    }
                    if (ch === '\\') {
                        next();
                        if (ch === 'u') {
                            var uffff = 0;
                            for (var i = 0; i < 4; i += 1) {
                                var hexChar = next();
                                if (!hexChar || !/^[0-9a-fA-F]$/.test(hexChar)) {
                                    error("Bad unicode escape in string");
                                }
                                var hex = parseInt(hexChar, 16);
                                uffff = uffff * 16 + hex;
                            }
                            s += String.fromCharCode(uffff);
                        } else if (ch === '"' || ch === '\\' || ch === '/') {
                            s += ch;
                        } else if (ch === 'b') {
                            s += '\b';
                        } else if (ch === 'f') {
                            s += '\f';
                        } else if (ch === 'n') {
                            s += '\n';
                        } else if (ch === 'r') {
                            s += '\r';
                        } else if (ch === 't') {
                            s += '\t';
                        } else {
                            error("Bad escape character '\\" + ch + "'");
                        }
                    } else {
                        s += ch;
                    }
                }
            }
            error("Unterminated string");
        }

        function parseNumber() {
            var n = '';

            // Optional minus
            if (ch === '-') {
                n = '-';
                next('-');
            }

            // Integer part
            if (ch === '0') {
                n += ch;
                next();
                // Leading zero followed by another digit is strictly forbidden in JSON!
                if (ch >= '0' && ch <= '9') {
                    error("Leading zero in number is invalid JSON");
                }
            } else if (ch >= '1' && ch <= '9') {
                while (ch >= '0' && ch <= '9') {
                    n += ch;
                    next();
                }
            } else {
                error("Bad number format, digit expected after sign");
            }

            // Fraction part
            if (ch === '.') {
                n += '.';
                next('.');
                if (!(ch >= '0' && ch <= '9')) {
                    error("Decimal point must be followed by at least one digit");
                }
                while (ch >= '0' && ch <= '9') {
                    n += ch;
                    next();
                }
            }

            // Exponent part
            if (ch === 'e' || ch === 'E') {
                n += ch;
                next();
                if (ch === '-' || ch === '+') {
                    n += ch;
                    next();
                }
                if (!(ch >= '0' && ch <= '9')) {
                    error("Exponent must be followed by at least one digit");
                }
                while (ch >= '0' && ch <= '9') {
                    n += ch;
                    next();
                }
            }

            var num = Number(n);
            if (!isFinite(num)) {
                error("Bad number value");
            }
            return num;
        }

        function parseWord() {
            switch (ch) {
                case 't':
                    next('t'); next('r'); next('u'); next('e');
                    return true;
                case 'f':
                    next('f'); next('a'); next('l'); next('s'); next('e');
                    return false;
                case 'n':
                    next('n'); next('u'); next('l'); next('l');
                    return null;
            }
            error("Unexpected word token '" + ch + "'");
        }

        function parseArray() {
            depth++;
            if (depth > MAX_DEPTH) {
                error("Excessive nesting depth (max " + MAX_DEPTH + ")");
            }
            var arr = [];
            if (ch === '[') {
                next('[');
                white();
                if (ch === ']') {
                    next(']');
                    depth--;
                    return arr;
                }
                while (ch) {
                    arr.push(parseValue());
                    white();
                    if (ch === ']') {
                        next(']');
                        depth--;
                        return arr;
                    }
                    if (ch !== ',') {
                        error("Expected ',' or ']' inside array");
                    }
                    next(',');
                    white();
                    if (ch === ']') {
                        error("Trailing comma in array is invalid JSON");
                    }
                }
            }
            error("Bad array syntax");
        }

        function parseObject() {
            depth++;
            if (depth > MAX_DEPTH) {
                error("Excessive nesting depth (max " + MAX_DEPTH + ")");
            }
            var obj = {};
            if (ch === '{') {
                next('{');
                white();
                if (ch === '}') {
                    next('}');
                    depth--;
                    return obj;
                }
                while (ch) {
                    if (ch !== '"') {
                        error("Object keys must be double-quoted strings");
                    }
                    var k = parseString();

                    // Security: Prototype pollution & duplicate key protection
                    if (k === "__proto__" || k === "constructor" || k === "prototype") {
                        error("Dangerous object key '" + k + "' rejected");
                    }
                    if (Object.prototype.hasOwnProperty.call(obj, k)) {
                        error("Duplicate object key '" + k + "' rejected");
                    }

                    white();
                    if (ch !== ':') {
                        error("Expected ':' after object key");
                    }
                    next(':');
                    obj[k] = parseValue();
                    white();
                    if (ch === '}') {
                        next('}');
                        depth--;
                        return obj;
                    }
                    if (ch !== ',') {
                        error("Expected ',' or '}' inside object");
                    }
                    next(',');
                    white();
                    if (ch === '}') {
                        error("Trailing comma in object is invalid JSON");
                    }
                }
            }
            error("Bad object syntax");
        }

        function parseValue() {
            white();
            switch (ch) {
                case '{': return parseObject();
                case '[': return parseArray();
                case '"': return parseString();
                case '-': return parseNumber();
                default:
                    return (ch >= '0' && ch <= '9') ? parseNumber() : parseWord();
            }
        }

        next();
        var result = parseValue();
        white();
        if (ch) {
            error("Syntax error, trailing characters after JSON");
        }
        return result;
    }

    return {
        getPresetFolder: getPresetFolder,
        parseJSONStrict: parseJSONStrict,
        serializeJSON: serializeJSON,

        listPresets: function() {
            var folder = getPresetFolder();
            if (!folder.exists) return [];
            var files = folder.getFiles("*.json");
            var names = [];
            for (var i = 0; i < files.length; i++) {
                var f = files[i];
                var name = decodeURI(f.name).replace(/\.json$/i, "");
                names.push(name);
            }
            return names;
        },

        savePreset: function(presetName, recipeId, paramValues, masterMode) {
            if (!presetName || !recipeId) return false;
            var cleanName = presetName.replace(/[^a-zA-Z0-9_\-\s]/g, "");
            if (cleanName === "") cleanName = "Preset";

            var folder = getPresetFolder();
            var file = new File(folder.fsName + "/" + cleanName + ".json");
            var data = {
                product: vac34_Config.PRODUCT_NAME,
                version: vac34_Config.VERSION,
                recipeId: recipeId,
                masterMode: !!masterMode,
                parameters: paramValues || {},
                createdAt: (new Date()).toUTCString()
            };

            try {
                file.encoding = "UTF-8";
                file.open("w");
                // Safe serialization: works with native JSON or fallback
                var jsonStr = (typeof JSON !== "undefined" && JSON && JSON.stringify) ? JSON.stringify(data) : serializeJSON(data);
                file.write(jsonStr);
                return true;
            } catch (e) {
                return false;
            } finally {
                try { file.close(); } catch (e) {}
            }
        },

        loadPreset: function(presetName) {
            if (!presetName) return null;
            var cleanName = presetName.replace(/[^a-zA-Z0-9_\-\s]/g, "");
            var folder = getPresetFolder();
            var file = new File(folder.fsName + "/" + cleanName + ".json");
            if (!file.exists) return null;

            var content = "";
            try {
                file.encoding = "UTF-8";
                file.open("r");
                content = file.read();
            } catch (e) {
                return null;
            } finally {
                try { file.close(); } catch (e) {}
            }

            try {
                // Strictly parse without eval
                var data = parseJSONStrict(content);

                // Strict Schema Validation
                if (!data || typeof data !== "object" || (data instanceof Array)) return null;
                if (!data.product || typeof data.product !== "string") return null;
                if (data.product !== vac34_Config.PRODUCT_NAME && data.product.indexOf("vac34") !== 0) return null;
                if (!data.recipeId || typeof data.recipeId !== "string") return null;

                // Validate that recipeId exists in catalog
                var recipe = vac34_RecipeRegistry.getRecipeById(data.recipeId);
                if (!recipe) return null;

                if (!data.parameters || typeof data.parameters !== "object" || (data.parameters instanceof Array)) return null;

                // Build lookup of known recipe parameters
                var knownParams = {};
                if (recipe.parameters) {
                    for (var p = 0; p < recipe.parameters.length; p++) {
                        knownParams[recipe.parameters[p].id] = recipe.parameters[p];
                    }
                }

                // Validate parameters dictionary values (must match known parameter definitions and types)
                for (var key in data.parameters) {
                    if (Object.prototype.hasOwnProperty.call(data.parameters, key)) {
                        if (!knownParams[key]) {
                            // Unknown parameter in preset for this recipe -> reject
                            return null;
                        }
                        var pDef = knownParams[key];
                        var val = data.parameters[key];
                        var t = typeof val;

                        if (pDef.type === "slider" || pDef.type === "angle") {
                            if (t !== "number" || !isFinite(val)) return null;
                            if (pDef.min !== undefined && val < pDef.min - 1000) return null;
                            if (pDef.max !== undefined && val > pDef.max + 1000) return null;
                        } else if (pDef.type === "checkbox") {
                            if (t !== "boolean" && t !== "number") return null;
                        } else {
                            if (t !== "number" && t !== "boolean" && t !== "string") return null;
                        }
                    }
                }

                return data;
            } catch (e) {
                return null;
            }
        }
    };
})();