# vac34_AE Architecture & Technical Feasibility Report

**Project:** vac34_AE — Master Expressions Studio  
**Initial Release:** v0.0.1  
**Target Host:** Adobe After Effects 2024 (v24.6.2, Windows 10 x64)  
**Date:** 2026-11-07  

---

## 1. Feasibility Investigation of Architecture Options

Before beginning development of v0.0.1, four potential architectures were evaluated against the technical requirements of After Effects 2024:

### A. ScriptUI + ExtendScript (Selected Baseline)
* **AE 2024 Compatibility:** Native, mature, first-class support in `Scripts/ScriptUI Panels/`.
* **Docking Behavior:** Seamless native dockable panel in After Effects workspace via `(thisObj instanceof Panel) ? thisObj : new Window(...)`.
* **Parameter Controls:** Direct DOM manipulation via `layer.property("Effects").addProperty(...)`, setting properties, setting keyframes, reading/writing `property.expression`.
* **Development & Deployment:** Single-file distributable JSX, modular multi-file source tree bundled at build time. Zero external runtimes, zero certificate signing bottlenecks.
* **Performance:** Instant startup, minimal memory footprint, direct in-process scripting engine.
* **Verdict:** **SELECTED**. It completely fulfills all functional requirements for v0.0.1 with zero deployment friction and 100% native dockability.

### B. CEP Panel (Common Extensibility Platform) + ExtendScript Bridge
* **AE 2024 Compatibility:** Supported via Chromium Embedded Framework.
* **Evaluation:** CEP introduces significant complexity: separate HTML5/CSS/JS frontend communicating across `CSInterface.evalScript()` to ExtendScript. Latency across the bridge slows down high-frequency parameter dragging. Distribution requires extension manifest registration (`CSXS`) and signing/debug mode flags.
* **Verdict:** REJECTED for v0.0.1. Overhead is unjustified for an expression orchestrator that directly benefits from tight ExtendScript DOM coupling.

### C. Native C++ After Effects SDK Effect Plugin (.aex)
* **AE 2024 Compatibility:** Supported via AE SDK 2024.
* **Evaluation:** A native C++ effect plugin computes image pixels on the GPU/CPU render pipeline (e.g. blur, distortion, pixel math). However, vac34_AE is an *expression-control studio and rig orchestrator*, not an image-processing pixel filter. A C++ plugin cannot act as a dockable workspace panel that inspects user layers, manages expressions on arbitrary layer transform properties, and provides a multi-recipe browser.
* **Verdict:** REJECTED. Scripting is the native and correct domain for layer expression management.

### D. UXP (Unified Extensibility Platform)
* **AE 2024 Compatibility:** In AE 2024 (24.x), UXP scripting and hybrid panels are still in transitional/partial availability compared to Photoshop/InDesign. UXP APIs for AE expression control inspection and effect manipulation have known limitations in 24.x compared to the mature ExtendScript OM.
* **Verdict:** REJECTED for v0.0.1. ExtendScript remains the standard production-proven API for AE 2024 panels.

---

## 2. System Architecture & Separation of Concerns

```text
vac34_ae_plugs/
│
├── src/
│   ├── core/         # Engine state, environment detection, event dispatcher
│   ├── adapters/     # AE DOM abstraction (Undo groups, property reflection, safe typing)
│   ├── controllers/  # Native Expression Control creation, naming & linking
│   ├── audio/        # Audio Amplitude discovery, signal routing & temporal sampling
│   ├── recipes/      # Declarative recipe registry across 13 core categories
│   ├── rigs/         # Multi-property composite rigs (Leader-Follower, Beat Master)
│   ├── presets/      # JSON configuration serialization, import/export
│   ├── diagnostics/  # Semantic validation, conflict detection, expression checker
│   └── panel/        # ScriptUI view, search filtering, dynamic parameter UI
│
├── build/            # Python/Node builder pipeline: lint, assemble, test, package
├── dist/             # Generated standalone JSX (vac34_AE.jsx)
└── release/          # Versioned release archives with SHA-256 manifests
```

---

## 3. Core Technical Decisions

### 3.1 Non-Destructive Expression Application
* **Additive Default:** Position expressions use `value + [dx, dy]`, Scale uses `[value[0] * sx, value[1] * sy]`, Rotation uses `value + rot`, preserving user keyframes and base layer transformations.
* **Ownership Tagging:** vac34-generated expressions contain a standardized header comment:
  `/* [vac34_AE: <recipe_id>] */`
  This enables safe detection, re-application, parameter update, and clean rollback without affecting user-written foreign expressions.
* **Conflict Policy:** If a foreign expression exists on the property, the user is warned and given an explicit choice (Wrap Additive or Abort).

### 3.2 Dual Controller Placement: Per-Layer vs Shared Master
1. **Per-Layer Mode:** Parameters are attached directly to the target layer under an effect group named `vac34 — <RecipeName>`. Ideal for independent animations.
2. **Shared Master Mode:** A dedicated controller null layer (`vac34_Master_Controls`) is created or reused. Multiple target layers link their expressions to the master null's sliders, providing unified control across compositions.

### 3.3 Audio Processing & Frequency Bands
* Raw amplitude is discovered from `Audio Amplitude` layers created by "Convert Audio to Keyframes".
* Real temporal envelopes (attack, decay, peak hold) use bounded backward frame sampling (max 30 frames) to guarantee non-blocking evaluation in AE's expression engine while avoiding the instantaneous threshold fallacy.

---

## 4. Verification and Deployment Strategy
* Dual deployment transaction:
  1. Live Host: `C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx`
  2. Backup Mirror: `V:\__STORE_V\_AE\install_AEPlugins\_install_healing\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx`
* Integrity verification: SHA-256 checksums of live and mirrored copies must be identical.
