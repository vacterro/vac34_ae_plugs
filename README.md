# vac34_AE — Master Expressions Studio

**Version:** 0.0.1  
**Target Host:** Adobe After Effects 2024 (24.x, Windows 10 x64)  
**Status:** MOCK_VERIFIED / BUILD_PASS / DEPLOY_PASS (Mirror Verified) / HOST_UNVERIFIED (Active User Desktop Session Protected)  

Unified dockable After Effects expression-control studio. Eliminates repetitive manual expression editing by providing an intuitive, parameter-driven workflow with native Expression Controls, audio reactivity, and preset management.

---

## Key Features

1. **Dockable ScriptUI Panel:** Native After Effects panel accessible via `Window > vac34_AE.jsx`.
2. **13 Behavioral Categories:** 
   - Audio Reactive (Beat Scale Pump, Audio Jump, Shake, Rotation Wobble, Strobe Flash, Temporal Attack/Release)
   - Scale (Sine Breathing, Squash & Stretch, Heartbeat, Elastic Overshoot)
   - Position (Smooth 2D Wiggle, Directional Drift, Circular & Elliptical Orbit)
   - Rotation (Continuous Spin, Pendulum Swing, Decaying Wobble)
   - Opacity (Sine Pulse, Strobe Blink, Candle Flicker)
   - Loops & Time (Cycle, Ping-Pong, Posterize Time)
   - Wiggle & Noise (Master Controlled Wiggle)
   - Physics & Inertia (Inertial Keyframe Bounce)
   - Rigging & Space (Multi-Layer Index Cascade)
   - Text & Shapes (Animated Numeric Counter)
   - Utilities (Safe Value Clamp, Remap)
3. **Dual Controller Placement:**
   - **Per-Layer Controls:** Independent sliders attached directly to target layers.
   - **Shared Master Null:** Synchronized parameter control across multiple layers via a dedicated `vac34_Master_Controls` null.
4. **Non-Destructive Expression Application:** Preserves original keyframes and base layer transformations using additive and multiplicative formulas.
5. **Preset System:** Save and load custom behavioral presets stored in user application data.
6. **Dual-Path Deployment:** Automated deployment to verified AE 2024 Support Files and recovery backup mirror with byte-identical SHA-256 verification.

---

## Directory Structure

```text
vac34_ae_plugs/
├── src/                  # Modular ExtendScript source files
├── sources/              # Canonical Bible source documents (V1, V2, V3)
├── catalog/              # Normalized recipes, provenance & quarantine logs
├── build/                # Python build pipeline & syntax validator
├── scripts/              # Management CLI (manage.py)
├── tests/                # Automated unit & integration acceptance tests
├── docs/                 # Architecture, user manual & deployment documentation
├── dist/                 # Deployed panel artifact (vac34_AE.jsx)
└── release/              # Versioned release packages (vac34_AE_v0.0.1.jsx)
```

---

## Quick Commands

```bash
# Build and run tests
python scripts/manage.py build

# Run all test suites
python scripts/manage.py test

# Build, package, and deploy to Live AE and Backup Mirror
python scripts/manage.py install

# Verify SHA-256 integrity across all installations
python scripts/manage.py verify
```
