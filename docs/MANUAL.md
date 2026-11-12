# vac34_AE — Master Expressions Studio User Manual

**Version:** 0.0.1  
**Target Host:** Adobe After Effects 2024 (24.x)  
**Distribution:** Dockable ScriptUI Panel (`vac34_AE.jsx`)  

---

## 1. Quick Start Guide

### Step 1: Launch After Effects
Open Adobe After Effects 2024.

### Step 2: Open the Studio Panel
In the top menu, navigate to:
`Window` → `vac34_AE.jsx`

The panel will open and can be docked anywhere in your workspace (e.g. alongside Effect Controls or Timeline).

### Step 3: Select Layers & Choose Behavior
1. Select one or more layers in your active composition.
2. Filter by category (e.g. `AUDIO REACTIVE`, `SCALE`, `POSITION`, `ROTATION`, `WIGGLE`) or type into the search box.
3. Click a behavior from the list (e.g. `Beat Scale Pump`, `Smooth 2D Wiggle`, `Inertial Keyframe Bounce`).

### Step 4: Adjust Parameters & Apply
1. Tweak sliders or type exact numbers in the dynamic Parameter Editor.
2. Choose controller mode:
   - **Per-Layer Controls:** Adds sliders directly to each selected layer.
   - **Shared Master Null:** Creates a `vac34_Master_Controls` null layer and links all selected layers to it.
3. Click **▶ Apply Behavior**.
4. The motion behavior evaluates immediately in your composition viewport!

### Step 5: Adjusting After Application
- You can tweak sliders inside the `vac34_AE` panel and click **Update**, or adjust the native Expression Controls directly in AE's **Effect Controls** panel.
- Even if you close the `vac34_AE` panel or send the project to another machine, the animation keeps working natively!

---

## 2. Audio-Reactive Workflow

1. In After Effects, select your audio layer and choose `Animation` → `Keyframe Assistant` → `Convert Audio to Keyframes`.
2. This creates an `Audio Amplitude` layer.
3. In `vac34_AE`, select the layers you want to animate to music.
4. Choose an audio behavior (e.g. `Beat Scale Pump`, `Audio Vertical Jump`, `Audio Reactive Shake`, `Audio Flash Strobe`).
5. Verify `Audio Amplitude` is selected in the **Audio Source Link** dropdown.
6. Click **▶ Apply Behavior**.

---

## 3. Preset System
- **Save Preset:** Dial in parameters, click **Save Preset**, and enter a custom name. Presets are saved as `.json` files in your user data directory (`%APPDATA%/vac34_AE/presets`).
- **Load Preset:** Click **Load Preset**, choose any saved preset from the dialog, and apply it to new layers.

---

## 4. Removal & Cleanup
- To remove a behavior without damaging your layer or keyframes, select the layer, pick the behavior in the panel, and click **Remove**.
- vac34 cleanly removes its expression controls and resets the expression.
