/*
 * vac34_AE — Master Expressions Studio
 * Fixed header/footer; content scrolls inside a bounded viewport parent.
 * Manual geometry keeps native preferred widths out of narrow dock layouts.
 * ponytail: ScriptUI Group paint clipping still needs real AE verification;
 * replace the viewport with paging if it leaks, never sibling overlays.
 */

var vac34_UIBuilder = (function() {
    // Historical values are load-bearing for the geometry snapshot tests
    // (contentTop = MARGIN + headerH + SECTION_GAP == 10 + 46 + 6).
    var MARGIN = 10;
    var SECTION_GAP = 6;
    var SCROLLBAR_WIDTH = 12;
    // Narrow dock size the layout must stay usable at (SAIHANDOFF §5).
    var MIN_W = 200;
    var MIN_H = 300;

    // ScriptUI dropdown selection is a ListItem (.index/.text) in the real
    // host; mocks and defensive callers may store a bare index. Both shapes
    // are read the same way.
    function dropdownIndex(dd) {
        if (!dd || dd.selection === null || dd.selection === undefined) return -1;
        if (typeof dd.selection === "number") return dd.selection;
        if (dd.selection.index !== undefined && dd.selection.index !== null) return dd.selection.index;
        return -1;
    }

    function dropdownText(dd) {
        if (!dd || !dd.items) return "";
        var idx = dropdownIndex(dd);
        if (idx < 0 || !dd.items[idx]) return "";
        return dd.items[idx].text || "";
    }

    function safeRemoveChildren(container) {
        if (!container || !container.children) return;
        var guard = 500;
        while (container.children.length > 0 && guard-- > 0) {
            var prevLen = container.children.length;
            try {
                if (typeof container.remove === "function") {
                    container.remove(container.children[0]);
                }
            } catch (e) {}
            if (container.children.length >= prevLen) {
                if (typeof container.children.shift === "function") {
                    container.children.shift();
                } else {
                    try {
                        container.remove(0);
                    } catch (e2) {}
                    if (container.children.length >= prevLen) {
                        break;
                    }
                }
            }
        }
    }

    return {
        build: function(thisObj) {
            var win = null;
            try {
                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.setStartupStage("2. Modules initialized");
                    vac34_Diagnostics.setStartupStage("3. UI container created");
                }
                var isDocked = (typeof Panel !== "undefined" && (thisObj instanceof Panel)) || (thisObj && thisObj.type === "panel");
                // Reentry guard: building into a panel that already hosts a
                // previous instance (script re-run) must clear it exactly once.
                if (isDocked && thisObj.__vac34Built) {
                    safeRemoveChildren(thisObj);
                }
                win = isDocked ? thisObj : new Window("palette", vac34_Config.PRODUCT_TITLE, undefined, { resizeable: true });
                if (isDocked && win.children && win.children.length > 0) {
                    safeRemoveChildren(win);
                }
                try {
                    win.__vac34Built = true;
                } catch (eTag) {}
                win.orientation = "column";
                win.alignChildren = ["fill", "top"];
                win.spacing = SECTION_GAP;
                win.margins = MARGIN;
                try {
                    win.minimumSize = [MIN_W, MIN_H];
                } catch (eMin) {}

                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.setStartupStage("4. Controls created");
                }

// Window layout: headerWrap (fixed top), viewportGroup (bounded scroll container),
                // footerWrap (fixed bottom). Creation order defines z-order: the
                // opaque footer/header panels draw over scrolling content, creating
                // fixed chrome. Manual geometry in updateChrome positions each.
                // Content is bounded: viewport height clamped, scroll offset moves
                // contentGroup inside. ScriptUI Group clipping verified separately.

                var headerWrap = win.add("group");
                headerWrap.orientation = "column";
                headerWrap.alignChildren = ["fill", "top"];
                headerWrap.spacing = 0;
                headerWrap.margins = 0;

                var footerWrap = win.add("group");
                footerWrap.orientation = "column";
                footerWrap.alignChildren = ["fill", "top"];
                footerWrap.spacing = 0;
                footerWrap.margins = 0;

                var footerGroup = footerWrap.add("panel", undefined, "");
                footerGroup.orientation = "column";
                footerGroup.alignChildren = ["fill", "top"];
                footerGroup.margins = 4;
                footerGroup.spacing = 4;

                var headerGroup = headerWrap.add("panel", undefined, "");
                headerGroup.orientation = "column";
                headerGroup.alignChildren = ["fill", "top"];
                headerGroup.margins = 4;
                headerGroup.spacing = 2;

                // Header: compact 2-row stacked layout
                // Row 1: product identity
                // Row 2: comp status, pin, audio, refresh
                var headerRow1 = headerGroup.add("group");
                headerRow1.orientation = "row";
                headerRow1.alignChildren = ["fill", "center"];

                var titleLbl = headerRow1.add("statictext", undefined, "⚡ " + vac34_Config.PRODUCT_NAME + " v" + vac34_Config.VERSION + " (" + vac34_Config.BUILD_ID + ")");
                try {
                    titleLbl.graphics.font = ScriptUI.newFont("Verdana", "BOLD", 10);
                } catch (e) {}

                var headerRow2 = headerGroup.add("group");
                headerRow2.orientation = "row";
                headerRow2.alignChildren = ["fill", "center"];
                headerRow2.spacing = 4;

                var compStatusLbl = headerRow2.add("statictext", undefined, "No Comp");
                try {
                    compStatusLbl.graphics.font = ScriptUI.newFont("Verdana", "REGULAR", 9);
                } catch (e) {}

                var btnCompPin = headerRow2.add("button", undefined, "Pin");
                btnCompPin.preferredSize = [36, 18];
                btnCompPin.helpTip = "Pin the active composition so panel focus never changes the target comp.";

                var audioStatusLbl = headerRow2.add("statictext", undefined, "AUDIO —");
                audioStatusLbl.alignment = ["right", "center"];

                var btnRefresh = headerRow2.add("button", undefined, "⟳");
                btnRefresh.preferredSize = [18, 18];
                btnRefresh.helpTip = "Refresh composition, audio and target status.";

                var lastResultLbl = headerGroup.add("statictext", undefined, "Last result: —");
                try {
                    lastResultLbl.graphics.font = ScriptUI.newFont("Verdana", "REGULAR", 9);
                } catch (e2) {}

                // Content inside bounded container. Manual geometry positions the
                // container; ScriptUI does not clip by default. Verify clipping
                // empirically in the host; replace with masking if needed.
                var viewportGroup = win.add("group");
                viewportGroup.orientation = "row";
                viewportGroup.alignChildren = ["fill", "top"];
                viewportGroup.spacing = 0;
                viewportGroup.margins = 0;

                var contentGroup = viewportGroup.add("group");
                contentGroup.orientation = "column";
                contentGroup.alignChildren = ["fill", "top"];
                contentGroup.spacing = SECTION_GAP;

                var vScroll = viewportGroup.add("scrollbar");
                vScroll.preferredSize = [SCROLLBAR_WIDTH, 80];
                vScroll.minimum = 0;
                vScroll.maximum = 0;
                vScroll.value = 0;
                vScroll.visible = false;
                vScroll.maximumSize = [SCROLLBAR_WIDTH, 10000];

                // --- SCROLLABLE CONTENT SECTIONS ---
                var targetGroup = contentGroup.add("group");
                targetGroup.orientation = "column";
                targetGroup.alignChildren = ["fill", "top"];
                targetGroup.spacing = 2;

                var targetRow = targetGroup.add("group");
                targetRow.orientation = "row";
                targetRow.alignChildren = ["fill", "center"];

                var targetModeDrop = targetRow.add("dropdownlist", undefined, [
                    "Target: Auto (Detect)",
                    "Target: Selected Property",
                    "Target: Recipe Default",
                    "Target: Pinned Target"
                ]);
                targetModeDrop.selection = 0;

                var btnPinTarget = targetRow.add("button", undefined, "Pin");
                btnPinTarget.preferredSize = [40, 20];
                btnPinTarget.helpTip = "Pin the currently selected property. Apply then always uses exactly this property.";

                var targetPreviewLbl = targetGroup.add("statictext", undefined, "Target: Auto (Detecting...)");
                try {
                    targetPreviewLbl.graphics.font = ScriptUI.newFont("Verdana", "REGULAR", 10);
                } catch (e3) {}

                var filterGroup = contentGroup.add("group");
                filterGroup.orientation = "row";
                filterGroup.alignChildren = ["fill", "center"];

                var searchInput = filterGroup.add("edittext", undefined, "");
                searchInput.helpTip = "Search behaviors...";

                var catDropdown = filterGroup.add("dropdownlist", undefined, vac34_RecipeRegistry.getCategories());
                catDropdown.selection = 0;

                var listGroup = contentGroup.add("group");
                listGroup.orientation = "column";
                listGroup.alignChildren = ["fill", "top"];

                var recipeList = listGroup.add("listbox", undefined, []);
                recipeList.preferredSize = [-1, 110];

                var descLbl = listGroup.add("statictext", undefined, "", { multiline: true });
                descLbl.preferredSize = [-1, 26];

                var audioGroup = contentGroup.add("panel", undefined, "Audio Source Link");
                audioGroup.orientation = "column";
                audioGroup.alignChildren = ["fill", "top"];
                audioGroup.margins = 6;
                audioGroup.spacing = 2;

                // Separate audio rows at all widths.
                var audioRow = audioGroup.add("group");
                audioRow.orientation = "row";
                audioRow.alignChildren = ["fill", "center"];

                var audioLyrLbl = audioRow.add("statictext", undefined, "Layer:");
                var audioLayerDrop = audioRow.add("dropdownlist", undefined, []);
                audioLayerDrop.selection = null;

                var audioRow2 = audioGroup.add("group");
                audioRow2.orientation = "row";
                audioRow2.alignChildren = ["fill", "center"];
                var audioChanLbl = audioRow2.add("statictext", undefined, "Channel:");
                var audioChanDrop = audioRow2.add("dropdownlist", undefined, ["Both Channels", "Left Channel", "Right Channel"]);
                audioChanDrop.selection = 0;

                var audioDetailLbl = audioGroup.add("statictext", undefined, "AUDIO —");
                try {
                    audioDetailLbl.graphics.font = ScriptUI.newFont("Verdana", "REGULAR", 10);
                } catch (e4) {}

                var modeGroup = contentGroup.add("group");
                modeGroup.orientation = "column";
                modeGroup.alignChildren = ["fill", "top"];

                var rbPerLayer = modeGroup.add("radiobutton", undefined, "Per-Layer Controls");
                rbPerLayer.value = true;
                var rbMaster = modeGroup.add("radiobutton", undefined, "Shared Master Null");

                var paramPanel = contentGroup.add("panel", undefined, "Parameters");
                paramPanel.orientation = "column";
                paramPanel.alignChildren = ["fill", "top"];
                paramPanel.margins = 8;

                var presetGroup = contentGroup.add("group");
                presetGroup.orientation = "row";
                presetGroup.alignChildren = ["fill", "center"];

                var btnSavePreset = presetGroup.add("button", undefined, "Save Preset");
                var btnLoadPreset = presetGroup.add("button", undefined, "Load Preset");

                // Diagnostics must not grow the fixed footer until it consumes
                // the narrow viewport. It is part of the scrollable content.
                var diagnosticsBox = contentGroup.add("edittext", undefined, "", { multiline: true, readonly: true });
                diagnosticsBox.preferredSize = [-1, 110];
                diagnosticsBox.visible = false;

                // Footer: status text row, then 2x2 button layout
                var statusBox = footerGroup.add("edittext", undefined, "Ready.", { multiline: true, readonly: true });
                statusBox.preferredSize = [-1, 34];

                var actionGroup = footerGroup.add("group");
                actionGroup.orientation = "column";
                actionGroup.alignChildren = ["fill", "top"];
                actionGroup.spacing = 2;

                var actionRow1 = actionGroup.add("group");
                actionRow1.orientation = "row";
                actionRow1.alignChildren = ["fill", "center"];
                actionRow1.spacing = 4;

                var actionRow2 = actionGroup.add("group");
                actionRow2.orientation = "row";
                actionRow2.alignChildren = ["fill", "center"];
                actionRow2.spacing = 4;

                var btnApply = actionRow1.add("button", undefined, "▶ Apply");
                var btnUpdate = actionRow1.add("button", undefined, "Update");
                var btnRemove = actionRow2.add("button", undefined, "Remove");
                var btnCopyDiag = actionRow2.add("button", undefined, "Copy Diagnostics");
                btnCopyDiag.helpTip = "Copy diagnostics; text stays available in the content viewport.";

                // -------------------------------------------------------------
                // UI STATE & CONTROLLER LOGIC
                // -------------------------------------------------------------
                var currentRecipes = [];
                var currentSelectedRecipe = null;
                var paramControlMap = {};
                var _selectedAudioName = null;
                var _selectedAudioIndex = null;
                var _audioSourceIndices = [];
                var _lastResult = "—";
                var _scrollTop = 0;
                var _chromeHeight = 0;
                var _viewportHeight = 0;
                var _contentTop = 0;
                var _layoutBusy = false;
                var _layoutPending = false;

                function getSelectedTargetMode() {
                    var idx = dropdownIndex(targetModeDrop);
                    if (idx === 1) return "SELECTED_PROPERTY";
                    if (idx === 2) return "RECIPE_DEFAULT";
                    if (idx === 3) return "PINNED";
                    return "AUTO";
                }

                function safeReflow(node) {
                    try {
                        if (node && node.layout && typeof node.layout.layout === "function") {
                            node.layout.layout(true);
                        }
                    } catch (eLayout) {}
                }

                // Measures natural heights, positions header/footer/viewport and scroll.
                // Recomputes scroll range on every call so recipe changes refresh it.
                function updateChrome(resetScroll) {
                    // Reentry guard: updateChrome may be re-entered by the reflow
                    // or resize notifications issued from within. Defer a follow-up
                    // pass instead of nesting, otherwise manual geometry and the
                    // scrollbar onChanging callback can re-enter each other.
                    if (_layoutBusy) { _layoutPending = true; return; }
                    _layoutBusy = true;
                    var winW, winH, headerH, footerH, contentH, viewportW, viewportH;
                    try { safeReflow(win); } catch (e0) {}
                    if (isDocked) {
                        try {
                            if (win && win.layout && typeof win.layout.resize === "function") {
                                win.layout.resize();
                            }
                        } catch (eResize) {}
                    }

                    try {
                        winW = win.size ? win.size[0] : 300;
                        winH = win.size ? win.size[1] : 400;
                    } catch (eSz) {}
                    headerH = (headerWrap && headerWrap.size && headerWrap.size[1]) ? headerWrap.size[1] : 50;
                    footerH = (footerWrap && footerWrap.size && footerWrap.size[1]) ? footerWrap.size[1] : 74;
                    contentH = (contentGroup && contentGroup.size && contentGroup.size[1]) ? contentGroup.size[1] : 300;

                    _chromeHeight = headerH + footerH;
                    _contentTop = MARGIN + headerH + SECTION_GAP;
                    var footerTop = winH - MARGIN - footerH;
                    _viewportHeight = Math.max(40, footerTop - _contentTop - SECTION_GAP);
                    _scrollTop = Math.max(0, contentH - _viewportHeight);

                    viewportW = Math.max(MIN_W - 2 * MARGIN - SCROLLBAR_WIDTH, winW - 2 * MARGIN);
                    viewportH = _viewportHeight;

                    try {
                        vScroll.maximum = _scrollTop;
                        if (resetScroll || vScroll.value > _scrollTop) {
                            vScroll.value = 0;
                        }
                        vScroll.preferredSize = [SCROLLBAR_WIDTH, Math.max(30, viewportH - 4)];
                        vScroll.visible = (_scrollTop > 0);
                    } catch (eScroll) {}

                    try {
                        // Clamp viewport to remaining height so natural content
                        // height can never push the fixed footer off-panel.
                        viewportGroup.preferredSize = [viewportW + SCROLLBAR_WIDTH, viewportH];
                        viewportGroup.maximumSize = [-1, viewportH];
                        viewportGroup.minimumSize = [viewportW + SCROLLBAR_WIDTH, viewportH];
                    } catch (eClamp) {}

                    try {
                        headerWrap.location = [MARGIN, MARGIN];
                        footerWrap.location = [MARGIN, footerTop];
                        viewportGroup.location = [MARGIN, _contentTop];
                    } catch (eLoc) {}

                    applyScroll();
                    _layoutBusy = false;
                    if (_layoutPending) {
                        _layoutPending = false;
                        updateChrome(resetScroll);
                    }
                }

                // Content top y relative to viewport root.
                function contentTopY() {
                    return 0;
                }

                function applyScroll() {
                    try {
                        var off = 0;
                        if (vScroll && typeof vScroll.value === "number") {
                            off = vScroll.value;
                        }
                        // Scroll offset moves content inside the viewport clamp.
                        contentGroup.location = [0, -off];
                    } catch (eScrollLoc) {}
                }

                vScroll.onChanging = function() {
                    applyScroll();
                };

                win.onResizing = function() {
                    updateChrome(false);
                };
                win.onResize = function() {
                    updateChrome(false);
                };

                function setStatus(statusCode, detail) {
                    _lastResult = statusCode;
                    try {
                        statusBox.text = detail ? (statusCode + ": " + detail) : statusCode;
                    } catch (eStatus) {}
                    try {
                        lastResultLbl.text = "Last result: " + statusCode;
                    } catch (eLast) {}
                    if (typeof vac34_Diagnostics !== "undefined" && vac34_Diagnostics.writePersistentLog) {
                        vac34_Diagnostics.writePersistentLog("UI OPERATION: " + statusCode + (detail ? (" -- " + detail) : ""));
                    }
                }

                function updateTargetPreview() {
                    if (typeof vac34_TargetResolver === "undefined") return;
                    var mode = getSelectedTargetMode();
                    if (mode === "PINNED") {
                        if (typeof vac34_AEDom === "undefined" || !vac34_AEDom.isTargetPinned()) {
                            targetPreviewLbl.text = "Target: none pinned (press Pin Target)";
                            return;
                        }
                        var info = vac34_AEDom.getPinnedTargetInfo();
                        var pinRes = vac34_AEDom.resolvePinnedTarget();
                        if (!pinRes.ok) {
                            targetPreviewLbl.text = "Pinned target unusable: " + (pinRes.message || pinRes.error);
                            return;
                        }
                        targetPreviewLbl.text = "Target (pinned): " + pinRes.path;
                        return;
                    }
                    var comp = getEffectiveComp();
                    var layers = (comp && vac34_AEDom.getSelectedLayers) ? vac34_AEDom.getSelectedLayers(comp) : [];
                    var summary = vac34_TargetResolver.getPreviewSummary(comp, layers, currentSelectedRecipe, mode);
                    targetPreviewLbl.text = summary;
                }

                // The composition every operation actually targets: the pinned
                // one when pinned, the AE active item otherwise.
                function getEffectiveComp() {
                    if (typeof vac34_AEDom !== "undefined" && vac34_AEDom.isCompPinned && vac34_AEDom.isCompPinned()) {
                        var pinned = vac34_AEDom.resolvePinnedComp();
                        if (pinned.ok) return pinned.comp;
                        return null;
                    }
                    return vac34_AEDom.getActiveComp();
                }

                function getAudioName() {
                    if (audioLayerDrop.selection) {
                        _selectedAudioName = dropdownText(audioLayerDrop) || _selectedAudioName;
                    }
                    return _selectedAudioName || vac34_Config.AUDIO_LAYER_NAME;
                }

                function syncAudioSelectionFromDropdown() {
                    var idx = dropdownIndex(audioLayerDrop);
                    if (idx >= 0) {
                        _selectedAudioName = dropdownText(audioLayerDrop) || _selectedAudioName;
                        _selectedAudioIndex = (idx < _audioSourceIndices.length) ? _audioSourceIndices[idx] : null;
                    }
                }

                function getAudioChan() {
                    return (audioChanDrop.selection) ? audioChanDrop.selection.text : "Both Channels";
                }

                function computeAudioStatus(comp) {
                    if (!comp) {
                        return { state: "NO COMP", valid: false, message: "No composition available." };
                    }
                    return vac34_AudioEngine.getAudioStatus(comp, getAudioName(), getAudioChan());
                }

                function refreshCompStatus() {
                    var comp = getEffectiveComp();
                    var pinnedComp = (typeof vac34_AEDom !== "undefined" && vac34_AEDom.isCompPinned()) ? vac34_AEDom.isCompPinned() : false;
                    if (comp) {
                        var selLayers = (vac34_AEDom.getSelectedLayers) ? vac34_AEDom.getSelectedLayers(comp) : [];
                        compStatusLbl.text = comp.name + " (" + selLayers.length + " sel)" + (pinnedComp ? " [Pinned]" : "");
                    } else {
                        compStatusLbl.text = pinnedComp ? "Pinned comp missing" : "No Active Comp";
                    }
                    try {
                        btnCompPin.text = pinnedComp ? "Unpin" : "Pin";
                    } catch (ePin) {}

                    // Audio source dropdown: restored by identity (comp layer
                    // index + name), never by display name alone. Duplicate
                    // display names never silently resolve to the first match;
                    // a vanished or ambiguous source is reported, not relinked.
                    var prevAudioName = _selectedAudioName;
                    var prevAudioIndex = _selectedAudioIndex;
                    syncAudioSelectionFromDropdown();
                    prevAudioName = _selectedAudioName;
                    prevAudioIndex = _selectedAudioIndex;

                    var audioSources = vac34_AudioEngine.findAudioLayers(comp);
                    if (typeof audioLayerDrop.removeAll === "function") {
                        audioLayerDrop.removeAll();
                    }
                    _audioSourceIndices = [];

                    var matchedIdx = -1;
                    var nameMatches = 0;
                    var firstNameMatchIdx = -1;
                    if (audioSources.length > 0) {
                        for (var i = 0; i < audioSources.length; i++) {
                            audioLayerDrop.add("item", audioSources[i].name);
                            _audioSourceIndices.push(audioSources[i].index);
                            if (prevAudioName && audioSources[i].name === prevAudioName) {
                                nameMatches++;
                                if (firstNameMatchIdx === -1) firstNameMatchIdx = i;
                                if (matchedIdx === -1 &&
                                    (prevAudioIndex === null || audioSources[i].index === prevAudioIndex)) {
                                    matchedIdx = i;
                                }
                            }
                        }
                        // Exactly one source with that name: safe to restore
                        // even if its layer index shifted during a reorder.
                        if (matchedIdx === -1 && nameMatches === 1) {
                            matchedIdx = firstNameMatchIdx;
                        }
                        // First open with no prior selection: default to the
                        // sole (or uniquely named) source; ambiguous names are
                        // never resolved to "the first one".
                        if (matchedIdx === -1 && prevAudioName === null) {
                            var seenNames = {};
                            var duplicateNames = false;
                            for (var u = 0; u < audioSources.length; u++) {
                                if (seenNames[audioSources[u].name]) { duplicateNames = true; break; }
                                seenNames[audioSources[u].name] = 1;
                            }
                            if (!duplicateNames) matchedIdx = 0;
                        }
                    }

                    var identityState = null;
                    if (audioSources.length === 0) {
                        audioLayerDrop.add("item", vac34_Config.AUDIO_LAYER_NAME);
                        _audioSourceIndices = [];
                        if (prevAudioName !== null) { identityState = "AUDIO_SOURCE_IDENTITY_LOST"; }
                        try { audioLayerDrop.selection = null; } catch (eSel0) { audioLayerDrop.selection = 0; }
                    } else if (matchedIdx !== -1) {
                        audioLayerDrop.selection = matchedIdx;
                        _selectedAudioIndex = _audioSourceIndices[matchedIdx];
                    } else if (nameMatches > 1 || prevAudioName === null) {
                        // Ambiguous: keep the name for a precise Apply failure, select nothing.
                        identityState = "AUDIO_SOURCE_AMBIGUOUS";
                        try { audioLayerDrop.selection = null; } catch (eSel1) {}
                    } else {
                        // Previously selected source vanished from this comp.
                        identityState = "AUDIO_SOURCE_IDENTITY_LOST";
                        audioLayerDrop.selection = null;
                    }

                    var audioStatus = computeAudioStatus(comp);
                    var statusState = identityState || audioStatus.state;
                    var statusLabel = statusState.replace(/_/g, " ");
                    audioStatusLbl.text = statusLabel;
                    audioDetailLbl.text = statusLabel + (audioStatus.message ? (" — " + audioStatus.message) : "");

                    updateTargetPreview();
                    updateChrome(false);
                }

                function refreshRecipeList() {
                    var selCat = (catDropdown.selection) ? catDropdown.selection.text : "All";
                    var query = searchInput.text;
                    currentRecipes = vac34_RecipeRegistry.filterRecipes(selCat, query);

                    if (typeof recipeList.removeAll === "function") {
                        recipeList.removeAll();
                    }
                    for (var i = 0; i < currentRecipes.length; i++) {
                        recipeList.add("item", currentRecipes[i].displayName);
                    }

                    if (currentRecipes.length > 0) {
                        setAuthoritativeSelection(0);
                    } else {
                        setAuthoritativeSelection(null);
                    }
                    updateChrome(false);
                }

                function clearParamPanel() {
                    safeRemoveChildren(paramPanel);
                    paramControlMap = {};
                    try {
                        if (paramPanel.layout) paramPanel.layout.layout(true);
                    } catch (ePanel) {}
                }

                function paramLabel(p) {
                    return (p && (p.label || p.name)) || "Parameter";
                }

// Metadata-driven editors: options -> dropdown (no intermediate
                // values), bool -> checkbox, everything else -> stacked numeric:
                // label row, controls row (range, slider, editbox, reset).
                function renderParameters(recipe, customValues) {
                    clearParamPanel();
                    if (!recipe || !recipe.parameters || recipe.parameters.length === 0) {
                        paramPanel.add("statictext", undefined, "No configurable parameters for this behavior.");
                        updateChrome(false);
                        return;
                    }

                    for (var i = 0; i < recipe.parameters.length; i++) {
                        (function(p) {
                            var unitSuffix = (p.unit && p.unit !== "") ? (" [" + p.unit + "]") : "";
                            var defaultVal = (p["default"] !== undefined) ? p["default"] : 0;
                            var initialVal = (customValues && customValues[p.id] !== undefined) ? customValues[p.id] : defaultVal;
                            var minVal = (p.min !== undefined) ? p.min : 0;
                            var maxVal = (p.max !== undefined) ? p.max : 100;

                            if (p.options && p.options.length > 0) {
                                var enumRow = paramPanel.add("group");
                                enumRow.orientation = "row";
                                enumRow.alignChildren = ["fill", "center"];
                                enumRow.spacing = 4;

                                var enumLabel = enumRow.add("statictext", undefined, paramLabel(p) + unitSuffix + ":");
                                var dropdown = enumRow.add("dropdownlist", undefined, []);
                                for (var o = 0; o < p.options.length; o++) {
                                    var opt = p.options[o];
                                    var optLabel = (typeof opt === "object") ? (opt.label || String(opt.value)) : String(opt);
                                    var optValue = (typeof opt === "object") ? opt.value : opt;
                                    dropdown.add("item", optLabel);
                                }
                                var selIdx = 0;
                                for (var m = 0; m < p.options.length; m++) {
                                    var ov = (typeof p.options[m] === "object") ? p.options[m].value : p.options[m];
                                    if (ov === initialVal) { selIdx = m; break; }
                                }
                                dropdown.selection = selIdx;

                                paramControlMap[p.id] = {
                                    param: p,
                                    editor: "enum",
                                    dropdown: dropdown,
                                    options: p.options,
                                    defaultVal: defaultVal,
                                    minVal: minVal,
                                    maxVal: maxVal
                                };
                                return;
                            }

                            if (p.type === "checkbox" || p.type === "bool") {
                                var chkRow = paramPanel.add("group");
                                chkRow.orientation = "row";
                                chkRow.alignChildren = ["fill", "center"];
                                chkRow.spacing = 4;

var checkbox = chkRow.add("checkbox", undefined, paramLabel(p) + unitSuffix + ":");
                                checkbox.value = !!initialVal;

                                paramControlMap[p.id] = {
                                    param: p,
                                    editor: "bool",
                                    checkbox: checkbox,
                                    defaultVal: defaultVal ? 1 : 0,
                                    minVal: minVal,
                                    maxVal: maxVal
                                };
                                return;
                            }

                            // Stacked numeric: label above controls
                            var numRow1 = paramPanel.add("group");
                            numRow1.orientation = "row";
                            numRow1.alignChildren = ["fill", "center"];
                            numRow1.spacing = 4;

                            var numLbl = numRow1.add("statictext", undefined, paramLabel(p) + unitSuffix + ":");
                            numLbl.preferredSize = [100, 20];

                            var numRow2 = paramPanel.add("group");
                            numRow2.orientation = "row";
                            numRow2.alignChildren = ["fill", "center"];
                            numRow2.spacing = 4;

                            var rangeLbl = numRow2.add("statictext", undefined, minVal + ".." + maxVal);
                            rangeLbl.preferredSize = [50, 20];

                            var slider = numRow2.add("slider", undefined, initialVal, minVal, maxVal);
                            slider.preferredSize = [100, 20];

                            var editbox = numRow2.add("edittext", undefined, String(initialVal));
                            editbox.preferredSize = [40, 20];

                            var resetBtn = numRow2.add("button", undefined, "↺");
                            resetBtn.preferredSize = [18, 18];
                            resetBtn.helpTip = "Reset to default (" + defaultVal + ")";

                            slider.onChanging = function() {
                                editbox.text = (p.type === "slider" && p.unit === "fps") ? Math.round(slider.value) : (Math.round(slider.value * 10) / 10);
                            };

                            editbox.onChange = function() {
                                var val = parseFloat(editbox.text);
                                if (!isNaN(val)) {
                                    slider.value = val;
                                }
                            };

                            resetBtn.onClick = function() {
                                slider.value = defaultVal;
                                editbox.text = String(defaultVal);
                            };

                            paramControlMap[p.id] = {
                                param: p,
                                editor: "numeric",
                                slider: slider,
                                editbox: editbox,
                                defaultVal: defaultVal,
                                minVal: minVal,
                                maxVal: maxVal
                            };
                        })(recipe.parameters[i]);
                    }

                    updateChrome(false);
                }

                function setAuthoritativeSelection(recipeOrIndex, customParamValues) {
                    var recipe = null;
                    var targetIndex = -1;

                    if (typeof recipeOrIndex === "number") {
                        targetIndex = recipeOrIndex;
                        if (targetIndex >= 0 && targetIndex < currentRecipes.length) {
                            recipe = currentRecipes[targetIndex];
                        }
                    } else if (recipeOrIndex && typeof recipeOrIndex === "object") {
                        recipe = recipeOrIndex;
                        for (var i = 0; i < currentRecipes.length; i++) {
                            if (currentRecipes[i].id === recipe.id) {
                                targetIndex = i;
                                break;
                            }
                        }
                        if (targetIndex === -1) {
                            if (catDropdown.selection && catDropdown.selection.index !== 0) {
                                catDropdown.selection = 0;
                            }
                            if (searchInput.text !== "") {
                                searchInput.text = "";
                            }
                            currentRecipes = vac34_RecipeRegistry.filterRecipes("All", "");
                            if (typeof recipeList.removeAll === "function") {
                                recipeList.removeAll();
                            }
                            for (var r = 0; r < currentRecipes.length; r++) {
                                recipeList.add("item", currentRecipes[r].displayName);
                                if (currentRecipes[r].id === recipe.id) {
                                    targetIndex = r;
                                }
                            }
                        }
                    }

                    currentSelectedRecipe = recipe;

                    if (recipe) {
                        if (targetIndex >= 0 && recipeList.items.length > targetIndex) {
                            recipeList.selection = targetIndex;
                        }
                        descLbl.text = recipe.description || "";
                        audioGroup.enabled = !!recipe.requiresAudio;
                        renderParameters(recipe, customParamValues);
                    } else {
                        recipeList.selection = null;
                        descLbl.text = (currentRecipes.length === 0) ? "No matching behaviors found." : "";
                        clearParamPanel();
                    }
                    updateTargetPreview();
                    updateChrome(false);
                }

                // Validates before Apply: enum selections must exist, numerics
                // are clamped into their declared range.
                function collectCurrentParameterValues() {
                    var values = {};
                    var errors = [];
                    for (var pId in paramControlMap) {
                        if (paramControlMap.hasOwnProperty(pId)) {
                            var ctrl = paramControlMap[pId];
                            var p = ctrl.param;

                            if (ctrl.editor === "enum") {
                                var optIdx = dropdownIndex(ctrl.dropdown);
                                if (optIdx < 0) {
                                    errors.push("Parameter '" + paramLabel(p) + "' has no selection.");
                                    continue;
                                }
                                var opt = ctrl.options[optIdx];
                                values[pId] = (typeof opt === "object") ? opt.value : opt;
                                continue;
                            }

                            if (ctrl.editor === "bool") {
                                values[pId] = ctrl.checkbox.value ? 1 : 0;
                                continue;
                            }

                            var val = parseFloat(ctrl.editbox.text);
                            if (isNaN(val)) val = ctrl.slider.value;
                            if (isNaN(val)) {
                                errors.push("Parameter '" + paramLabel(p) + "' is not a number.");
                                continue;
                            }
                            if (ctrl.minVal !== undefined && ctrl.minVal !== null && val < ctrl.minVal) {
                                val = ctrl.minVal;
                                ctrl.editbox.text = String(val);
                            }
                            if (ctrl.maxVal !== undefined && ctrl.maxVal !== null && val > ctrl.maxVal) {
                                val = ctrl.maxVal;
                                ctrl.editbox.text = String(val);
                            }
                            values[pId] = val;
                        }
                    }
                    return { values: values, errors: errors };
                }

                function buildDiagnosticsText() {
                    var lines = [];
                    lines.push("vac34_AE diagnostics");
                    lines.push("build: " + vac34_Config.VERSION + " (" + vac34_Config.BUILD_ID + ")");
                    try {
                        var comp = getEffectiveComp();
                        lines.push("composition: " + (comp ? comp.name : "none") + (vac34_AEDom.isCompPinned() ? " [pinned]" : ""));
                    } catch (eComp) {}
                    try {
                        lines.push("target mode: " + getSelectedTargetMode());
                        if (vac34_AEDom.isTargetPinned()) {
                            var info = vac34_AEDom.getPinnedTargetInfo();
                            if (info) {
                                lines.push("pinned target: " + info.compName + " > " + info.path);
                            }
                        }
                        var pinRes = null;
                        if (getSelectedTargetMode() === "PINNED") {
                            pinRes = vac34_AEDom.resolvePinnedTarget();
                            lines.push("pinned target state: " + (pinRes.ok ? "resolved" : (pinRes.error || "unresolved")));
                        }
                    } catch (ePin2) {}
                    try {
                        var aStat = computeAudioStatus(getEffectiveComp());
                        lines.push("audio: " + aStat.state + " — " + (aStat.message || ""));
                    } catch (eAudio) {}
                    try {
                        lines.push("recipe: " + (currentSelectedRecipe ? currentSelectedRecipe.id : "none"));
                        var pVals = collectCurrentParameterValues();
                        lines.push("parameters: " + JSON.stringify(pVals.values) + (pVals.errors.length ? (" errors: " + pVals.errors.join("; ")) : ""));
                    } catch (eParams) {}
                    lines.push("last result: " + _lastResult);
                    if (typeof vac34_Diagnostics !== "undefined" && vac34_Diagnostics.getStartupLog) {
                        try {
                            var log = vac34_Diagnostics.getStartupLog();
                            lines.push("startup log entries: " + log.length + " (last: " + (log[log.length - 1] ? log[log.length - 1].stage : "?") + ")");
                        } catch (eLog) {}
                    }
                    return lines.join("\n");
                }

                // -------------------------------------------------------------
                // UNIFIED OPERATION RUNNER
                // Every operation records its start, validates composition,
                // target, recipe and audio, runs the engine, converts the
                // structured result into a visible status and logs diagnostics.
                // No operation can end silently or on an uncaught exception.
                // -------------------------------------------------------------
                function executeUiOperation(kind) {
                    setStatus("RUNNING", kind + " started");
                    try {
                        if (!currentSelectedRecipe) {
                            setStatus("NO_RECIPE", "Select a behavior first.");
                            return;
                        }

                        var comp = getEffectiveComp();
                        if (!comp) {
                            var noCompMsg = (typeof vac34_AEDom !== "undefined" && vac34_AEDom.isCompPinned())
                                ? "Pinned composition is missing or was deleted."
                                : "No active composition open in After Effects.";
                            setStatus("COMP_MISSING", noCompMsg);
                            return;
                        }

                        var layers = vac34_AEDom.getSelectedLayers(comp);
                        var pVals = collectCurrentParameterValues();
                        if (pVals.errors.length > 0) {
                            setStatus("PARAMETER_INVALID", pVals.errors.join(" "));
                            return;
                        }
                        var isMaster = rbMaster.value;
                        var targetMode = getSelectedTargetMode();
                        var recipe = currentSelectedRecipe;

                        if (kind === "apply") {
                            if (recipe.requiresAudio) {
                                var audioStatus = computeAudioStatus(comp);
                                if (!audioStatus.valid) {
                                    setStatus(audioStatus.state, audioStatus.message);
                                    return;
                                }
                            }
                            if (targetMode === "PINNED" && (!vac34_AEDom.isTargetPinned())) {
                                setStatus("TARGET_NOT_PINNED", "Pin a target property first (select a property, press Pin Target).");
                                return;
                            }
                            // Never silently fall back to the default-named
                            // layer: a lost or ambiguous audio source must fail
                            // validation, not attach itself to another layer.
                            var audioName = getAudioName();
                            var audioChan = getAudioChan();
                            var res = vac34_Engine.applyRecipe(comp, layers, recipe, pVals.values, isMaster, audioName, audioChan, targetMode);
                            presentResult(res);
                            updateTargetPreview();
                            return;
                        }

                        if (kind === "update") {
                            var upRes = vac34_Engine.updateParameters(comp, layers, recipe, pVals.values, isMaster, targetMode);
                            presentResult(upRes);
                            updateTargetPreview();
                            return;
                        }

                        if (kind === "remove") {
                            var rmRes = vac34_Engine.removeRecipe(comp, layers, recipe, null, targetMode === "PINNED" ? "PINNED" : targetMode);
                            presentResult(rmRes);
                            updateTargetPreview();
                            return;
                        }

                        setStatus("UNKNOWN_OPERATION", kind);
                    } catch (opErr) {
                        setStatus("UNEXPECTED_ERROR",
                            (opErr && (opErr.message || opErr.toString())) + (opErr && opErr.line ? (" (line " + opErr.line + ")") : ""));
                    }
                    updateTargetPreview();
                }

                function presentResult(res) {
                    if (!res) {
                        setStatus("UNEXPECTED_ERROR", "Engine returned no result.");
                        return;
                    }
                    var status = res.status || (res.ok ? "OK" : "FAILED");
                    var detail = res.message || "";
                    if (res.warnings && res.warnings.length > 0) {
                        detail += (detail ? " | " : "") + res.warnings.join(" | ");
                    }
                    if (res.errors && res.errors.length > 0) {
                        detail += (detail ? " | " : "") + res.errors.join(" | ");
                    }
                    setStatus(status, detail);
                }

                // --- EVENT WIRING ---
                btnRefresh.onClick = function() {
                    refreshCompStatus();
                };

                btnCompPin.onClick = function() {
                    var comp = vac34_AEDom.getActiveComp();
                    if (vac34_AEDom.isCompPinned()) {
                        vac34_AEDom.clearCompPin();
                        setStatus("COMP_UNPINNED", "Composition pin released.");
                    } else {
                        if (!comp) {
                            setStatus("COMP_MISSING", "No active composition to pin.");
                            return;
                        }
                        var pinRes = vac34_AEDom.pinComp(comp);
                        if (pinRes.ok) {
                            setStatus("COMP_PINNED", comp.name + " pinned. Panel focus will not change the target composition.");
                        } else {
                            setStatus("COMP_PIN_FAILED", pinRes.message || pinRes.error);
                            return;
                        }
                    }
                    refreshCompStatus();
                };

                btnPinTarget.onClick = function() {
                    var comp = getEffectiveComp();
                    if (!comp) {
                        setStatus("COMP_MISSING", "No composition available to pin a target in.");
                        return;
                    }
                    var selected = (typeof vac34_TargetResolver !== "undefined") ? vac34_TargetResolver.getSelectedProperties(comp) : [];
                    if (selected.length === 0) {
                        setStatus("TARGET_MISSING", "Select exactly one expression-capable property in the timeline first.");
                        return;
                    }
                    if (selected.length > 1) {
                        setStatus("TARGET_AMBIGUOUS", selected.length + " properties are selected; pin requires exactly one.");
                        return;
                    }
                    var pinRes = vac34_AEDom.pinTarget(comp, selected[0]);
                    if (pinRes.ok) {
                        targetModeDrop.selection = 3;
                        setStatus("TARGET_PINNED", "Pinned " + pinRes.path);
                    } else {
                        setStatus("TARGET_PIN_FAILED", pinRes.message || pinRes.error);
                    }
                    updateTargetPreview();
                };

                targetModeDrop.onChange = function() {
                    updateTargetPreview();
                };

                catDropdown.onChange = function() {
                    refreshRecipeList();
                };

                searchInput.onChanging = function() {
                    refreshRecipeList();
                };

                recipeList.onChange = function() {
                    if (recipeList.selection) {
                        var idx = recipeList.selection.index;
                        setAuthoritativeSelection(idx);
                    } else {
                        setAuthoritativeSelection(null);
                    }
                };

                audioLayerDrop.onChange = function() {
                    syncAudioSelectionFromDropdown();
                    var comp = getEffectiveComp();
                    var audioStatus = computeAudioStatus(comp);
                    audioStatusLbl.text = audioStatus.state.replace(/_/g, " ");
                    audioDetailLbl.text = audioStatus.state.replace(/_/g, " ") + (audioStatus.message ? (" — " + audioStatus.message) : "");
                };

                audioChanDrop.onChange = function() {
                    refreshCompStatus();
                };

                btnApply.onClick = function() {
                    executeUiOperation("apply");
                };

                btnUpdate.onClick = function() {
                    executeUiOperation("update");
                };

                btnRemove.onClick = function() {
                    executeUiOperation("remove");
                };

                btnCopyDiag.onClick = function() {
                    var text = buildDiagnosticsText();
                    var writtenPath = null;
                    try {
                        if (typeof Folder !== "undefined" && typeof File !== "undefined" && Folder.userData) {
                            var diagDir = new Folder(Folder.userData.fsName + "/vac34_AE");
                            if (!diagDir.exists) diagDir.create();
                            var diagFile = new File(diagDir.fsName + "/diagnostics.txt");
                            diagFile.encoding = "UTF-8";
                            diagFile.open("w");
                            diagFile.write(text);
                            diagFile.close();
                            writtenPath = diagFile.fsName;
                        }
                    } catch (eDiag) {}
                    try {
                        diagnosticsBox.text = text;
                        diagnosticsBox.visible = true;
                    } catch (eBox) {}
                    updateChrome(false);
                    setStatus("DIAGNOSTICS",
                        (writtenPath ? ("Written to " + writtenPath + ". ") : "") +
                        "Text is selected below — Ctrl+C copies it to the clipboard.");
                    try {
                        if (diagnosticsBox && typeof diagnosticsBox.textselection === "string") {
                            diagnosticsBox.textselection = "0," + String(text.length);
                        }
                    } catch (eSel2) {}
                };

                btnSavePreset.onClick = function() {
                    if (!currentSelectedRecipe) {
                        setStatus("NO_RECIPE", "Select a behavior before saving preset.");
                        return;
                    }
                    var name = prompt("Enter Preset Name:", currentSelectedRecipe.displayName + " Custom");
                    if (name) {
                        var pVals = collectCurrentParameterValues();
                        if (pVals.errors.length > 0) {
                            setStatus("PARAMETER_INVALID", pVals.errors.join(" "));
                            return;
                        }
                        var saved = vac34_PresetManager.savePreset(name, currentSelectedRecipe.id, pVals.values, rbMaster.value);
                        if (saved) {
                            setStatus("PRESET_SAVED", "Preset '" + name + "' saved successfully.");
                        } else {
                            setStatus("PRESET_SAVE_FAILED", "Failed to save preset.");
                        }
                    }
                };

                btnLoadPreset.onClick = function() {
                    var presets = vac34_PresetManager.listPresets();
                    if (presets.length === 0) {
                        setStatus("NO_PRESETS", "No saved presets found in user folder.");
                        return;
                    }
                    var pWin = new Window("dialog", "Load Preset");
                    pWin.orientation = "column";
                    pWin.alignChildren = ["fill", "top"];
                    var pList = pWin.add("listbox", undefined, presets);
                    pList.selection = 0;
                    pList.preferredSize = [200, 150];

                    var pBtnRow = pWin.add("group");
                    var btnOk = pBtnRow.add("button", undefined, "Load");
                    var btnCancel = pBtnRow.add("button", undefined, "Cancel");

                    btnOk.onClick = function() {
                        if (pList.selection) {
                            var pName = pList.selection.text;
                            var pData = vac34_PresetManager.loadPreset(pName);
                            if (pData) {
                                var rec = vac34_RecipeRegistry.getRecipeById(pData.recipeId);
                                if (rec) {
                                    setAuthoritativeSelection(rec, pData.parameters);
                                    rbMaster.value = !!pData.masterMode;
                                    rbPerLayer.value = !pData.masterMode;
                                    setStatus("PRESET_LOADED", "Loaded preset '" + pName + "' (" + rec.displayName + ").");
                                } else {
                                    setStatus("PRESET_LOAD_FAILED", "Preset references unknown behavior '" + pData.recipeId + "'.");
                                }
                            } else {
                                setStatus("PRESET_LOAD_FAILED", "Invalid or corrupted preset file.");
                            }
                        }
                        pWin.close();
                    };
                    btnCancel.onClick = function() { pWin.close(); };
                    pWin.show();
                };

                win.setAuthoritativeSelection = setAuthoritativeSelection;
                win.getCurrentSelectedRecipe = function() { return currentSelectedRecipe; };
                win.getParamControlMap = function() { return paramControlMap; };
                win.getContentGroup = function() { return contentGroup; };
                win.getHeaderGroup = function() { return headerWrap; };
                win.getFooterGroup = function() { return footerWrap; };
                win.getScrollbar = function() { return vScroll; };
                win.getViewportGroup = function() { return viewportGroup; };
                win.refreshLayout = updateChrome;
                win.refreshCompStatus = refreshCompStatus;
                win.collectParameterValues = collectCurrentParameterValues;
                win.getAudioStatusLabel = function() { return audioStatusLbl; };
                win.executeUiOperation = executeUiOperation;
                win.getLastResult = function() { return _lastResult; };
                win.getStatusText = function() { return statusBox.text; };
                win.getGeometry = function() {
                    var W = (win && win.size && win.size[0]) ? win.size[0] : MIN_W;
                    var H = (win && win.size && win.size[1]) ? win.size[1] : MIN_H;
                    return {
                        panel: { width: W, height: H },
                        header: { y: MARGIN, height: (headerWrap && headerWrap.size && headerWrap.size[1]) || 50 },
                        viewport: { y: _contentTop, width: (viewportGroup && viewportGroup.size && viewportGroup.size[0]) || (W - 2 * MARGIN),
                            height: _viewportHeight },
                        footer: { y: H - MARGIN - ((footerWrap && footerWrap.size && footerWrap.size[1]) || 74),
                            height: (footerWrap && footerWrap.size && footerWrap.size[1]) || 74 },
                        scroll: { max: _scrollTop, value: (vScroll && typeof vScroll.value === "number") ? vScroll.value : 0,
                            visible: (vScroll && vScroll.visible) || false },
                        minimums: { width: MIN_W, height: MIN_H }
                    };
                };

                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.setStartupStage("5. Recipes loaded");
                }
                refreshCompStatus();
                refreshRecipeList();

                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.setStartupStage("6. Initial layout complete");
                }
                updateChrome(true);

                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.setStartupStage("7. Panel ready");
                }
                try {
                    statusBox.text = "Ready.";
                } catch (eReady) {}

                return win;
            } catch (startupErr) {
                var failedStage = (typeof vac34_Diagnostics !== "undefined") ? vac34_Diagnostics.getCurrentStartupStage() : "3. UI container created";
                if (typeof vac34_Diagnostics !== "undefined") {
                    vac34_Diagnostics.recordStartupError(failedStage, startupErr);
                }

                if (!win && thisObj && ((typeof Panel !== "undefined" && (thisObj instanceof Panel)) || (thisObj && thisObj.type === "panel"))) {
                    win = thisObj;
                } else if (!win) {
                    try {
                        win = new Window("palette", (typeof vac34_Config !== "undefined" ? vac34_Config.PRODUCT_NAME : "vac34_AE") + " [Diagnostic Mode]", undefined, { resizeable: true });
                    } catch (wErr) {}
                }

                if (win) {
                    try {
                        safeRemoveChildren(win);
                        win.orientation = "column";
                        win.alignChildren = ["fill", "top"];
                        win.spacing = SECTION_GAP;
                        win.margins = MARGIN;

                        var errGroup = win.add("panel", undefined, "⚡ vac34_AE — Initialization Failure");
                        errGroup.orientation = "column";
                        errGroup.alignChildren = ["fill", "top"];
                        errGroup.margins = 10;
                        errGroup.spacing = 6;

                        var errTitle = errGroup.add("statictext", undefined, "Halted at: " + failedStage);
                        try {
                            errTitle.graphics.font = ScriptUI.newFont("Verdana", "BOLD", 11);
                        } catch (eFont) {}

                        var errMsg = (startupErr && (startupErr.message || startupErr.toString())) || "Unknown error";
                        var errLine = (startupErr && startupErr.line) ? ("\nLine: " + startupErr.line) : "";
                        var errDetails = errGroup.add("edittext", undefined, "Error: " + errMsg + errLine + "\nSee logs/startup_diagnostics.log for details.", { multiline: true, readonly: true });
                        errDetails.preferredSize = [-1, 75];

                        var retryBtn = errGroup.add("button", undefined, "Retry Startup");
                        retryBtn.onClick = function() {
                            try {
                                vac34_UIBuilder.build(thisObj);
                            } catch (reErr) {
                                if (typeof alert !== "undefined") alert("Retry failed: " + (reErr.message || reErr));
                            }
                        };

                        if (win.layout) {
                            win.layout.layout(true);
                            win.layout.resize();
                        }
                    } catch (recErr) {}
                }
                throw startupErr;
            }
        }
    };
})();
