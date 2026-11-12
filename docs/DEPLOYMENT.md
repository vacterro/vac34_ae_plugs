# vac34_AE Deployment & Mirror Maintenance Specification

**Product Version:** v0.0.1  
**Build Status:** MOCK_VERIFIED / BUILD_PASS / DEPLOY_PASS (Mirror Verified) / HOST_UNVERIFIED  

---

## 0. Current Verification & Integrity State

- **Unit & Hardening Tests:** 37/37 PASS (Node.js ExtendScript mock runtime).
- **Clean Export & Rebuild:** 10/10 PASS (Self-contained standalone archive).
- **Backup Recovery Mirror:** SYNCHRONIZED (`V:\__STORE_V\_AE\install_AEPlugins\_install_healing\...`).
- **Live AE Panel (`C:\Program Files`):** Requires elevated Administrator or `vac34` permissions. Synchronizable via `python scripts/manage.py repair-mirror`.
- **Live Host Verification:** HOST_UNVERIFIED. After Effects 2024 (PID 16060) is currently running on the user's active desktop session; non-invasive execution rules strictly prohibit hijacking desktop focus or UI during automated tasks.

---

## 1. Authoritative Paths

### Primary Development Workspace
```text
V:\___VAC\__K\__CODE\_PLUG_SCRIPT\vac34_ae_plugs\
```

### Live Host Installation (Adobe After Effects 2024)
```text
C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx
```

### Required Backup & Recovery Mirror
```text
V:\__STORE_V\_AE\install_AEPlugins\_install_healing\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx
```

---

## 2. Integrity Guarantee
- Every build validates that the Live AE installed panel and the Backup Mirror copy have **byte-identical SHA-256 hashes**.
- Current Verified SHA-256: `d485dc443518eefa869311a57e40ea98aca65ea3bbaf080a5e6dec4887082247`

---

## 3. Maintenance & CLI Commands

From the workspace root:

```bash
# Build and run tests
python scripts/manage.py build

# Run all unit and scenario test suites
python scripts/manage.py test

# Ingest and validate markdown bibles
python scripts/manage.py validate

# Build, test, package, and deploy to Live AE + Mirror
python scripts/manage.py install

# Verify byte-identical checksums across all installations
python scripts/manage.py verify

# Disaster recovery: restore Live AE from verified backup mirror
python scripts/manage.py repair-mirror

# Clean removal from host and mirror
python scripts/manage.py uninstall
```
