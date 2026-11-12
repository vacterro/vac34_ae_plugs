var app = { name: "Mock", version: "Mock", project: { activeItem: null, numItems: 0 } };
var Panel = function() {};
var Window = function() {};
var Folder = { userData: { fsName: "C:/tmp" }, temp: { fsName: "C:/tmp" } };
var File = function() { this.exists = function() { return false; }; this.create = function() {}; this.open = function() {}; this.write = function() {}; this.close = function() {}; };

// Load the bundle
var fs = require('fs');
var bundle = fs.readFileSync('dist/vac34_AE.jsx', 'utf8');
new Function('thisObj', bundle)(null);

// Run smoke test
var results = vac34_HostSmokeTest.run(null);
JSON.stringify(results, null, 2);
