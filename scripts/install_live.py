#!/usr/bin/env python3
"""
vac34_AE Elevated Live Installer Script
Implements the 11-step reliable deployment and verification procedure:
 1. Discover actual AE 2024 installation.
 2. Verify source artifact.
 3. Verify source SHA-256 against release manifest.
 4. Verify ownership of existing file.
 5. Save verified rollback copy.
 6. Perform authorized elevated installation.
 7. Verify new Live SHA-256.
 8. Synchronize Backup Mirror.
 9. Verify Backup Mirror SHA-256.
 10. Write deployment report.
 11. Return correct exit code (0 on success, nonzero on error).
"""

import os
import sys
import json
import shutil
import hashlib

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(WORKSPACE_ROOT, "build")
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
if BUILD_DIR not in sys.path:
    sys.path.insert(0, BUILD_DIR)

try:
    from build.builder import (
        discover_ae_install_dir,
        compute_sha256,
        find_installed_instances,
        MIRROR_INSTALL_DIR,
        DIST_FILENAME,
        DeploymentState
    )
except (ImportError, ModuleNotFoundError):
    import importlib.util
    builder_path = os.path.join(BUILD_DIR, "builder.py")
    spec = importlib.util.spec_from_file_location("builder", builder_path)
    if spec is None or spec.loader is None:
        raise
    builder = importlib.util.module_from_spec(spec)
    sys.modules["builder"] = builder
    spec.loader.exec_module(builder)

    discover_ae_install_dir = builder.discover_ae_install_dir
    compute_sha256 = builder.compute_sha256
    find_installed_instances = builder.find_installed_instances
    MIRROR_INSTALL_DIR = builder.MIRROR_INSTALL_DIR
    DIST_FILENAME = builder.DIST_FILENAME
    DeploymentState = builder.DeploymentState
from scripts.manage import verify_vac34_ownership

def _record_deploy_blocked(target_live: str, dist_sha: str, err_msg: str):
    target_mirror = os.path.join(MIRROR_INSTALL_DIR, DIST_FILENAME)
    mirror_parent = os.path.dirname(target_mirror)
    try:
        os.makedirs(mirror_parent, exist_ok=True)
        dist_file = os.path.join(WORKSPACE_ROOT, "dist", DIST_FILENAME)
        shutil.copy2(dist_file, target_mirror)
    except Exception:
        pass

    live_sha = compute_sha256(target_live) if os.path.exists(target_live) else None
    mirror_sha = compute_sha256(target_mirror) if os.path.exists(target_mirror) else None

    deploy_results = {
        "state": DeploymentState.DEPLOY_BLOCKED,
        "live_installed": False,
        "mirror_installed": (mirror_sha == dist_sha),
        "hashes_match": False,
        "live_path": target_live,
        "mirror_path": target_mirror,
        "live_sha256": live_sha,
        "mirror_sha256": mirror_sha,
        "live_error": err_msg,
        "mirror_error": None,
        "installed_instances": find_installed_instances()
    }
    log_dir = os.path.join(WORKSPACE_ROOT, "logs")
    os.makedirs(log_dir, exist_ok=True)
    report_path = os.path.join(log_dir, "deployment_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(deploy_results, f, indent=2)

def install_live_and_mirror() -> int:
    print("=== vac34_AE Live & Mirror Installation Procedure ===")
    
    # Step 1: Discover AE 2024 installation
    live_dir = discover_ae_install_dir()
    target_live = os.path.join(live_dir, DIST_FILENAME)
    print(f"[1/11] Discovered AE 2024 ScriptUI directory: {live_dir}")
    print(f"       Live target path: {target_live}")

    # Step 2: Check source artifact
    dist_file = os.path.join(WORKSPACE_ROOT, "dist", DIST_FILENAME)
    if not os.path.exists(dist_file):
        print(f"[ERROR] Source artifact missing at: {dist_file}")
        print("Run python build/builder.py first.")
        return 1
    dist_size = os.path.getsize(dist_file)
    if dist_size < 5000:
        print(f"[ERROR] Source artifact size abnormally small ({dist_size} bytes)")
        return 1
    print(f"[2/11] Source artifact verified: {dist_file} ({dist_size} bytes)")

    # Step 3: Check SHA-256 against release manifest
    manifest_file = os.path.join(WORKSPACE_ROOT, "release", "build_manifest.json")
    if not os.path.exists(manifest_file):
        print(f"[ERROR] Release manifest missing at: {manifest_file}")
        return 1
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    expected_sha = manifest.get("sha256")
    dist_sha = compute_sha256(dist_file)
    if dist_sha != expected_sha:
        print(f"[ERROR] Source artifact SHA-256 ({dist_sha}) does not match manifest ({expected_sha})")
        return 1
    print(f"[3/11] Source artifact SHA-256 verified: {dist_sha}")

    # Step 4: Verify ownership of existing file
    if os.path.exists(target_live):
        if not verify_vac34_ownership(target_live):
            print(f"[FATAL] Target {target_live} exists but is not a recognized vac34 script.")
            print("Refusing to overwrite foreign third-party file.")
            return 1
        print(f"[4/11] vac34 ownership verified on existing live file.")
    else:
        print(f"[4/11] Target live file does not exist yet (clean install).")

    # Step 5: Save rollback copy
    live_backed_up = False
    if os.path.exists(target_live):
        bak_file = target_live + ".bak"
        try:
            shutil.copy2(target_live, bak_file)
            bak_sha = compute_sha256(bak_file)
            orig_sha = compute_sha256(target_live)
            if bak_sha != orig_sha:
                print("[ERROR] Backup integrity verification failed (hash mismatch).")
                return 1
            live_backed_up = True
            print(f"[5/11] Verified rollback copy saved to: {bak_file}")
        except PermissionError as pe:
            print(f"[FATAL] Permission denied creating backup copy: {pe}")
            print("Administrator elevation required. Run scripts/install_admin.cmd as Administrator.")
            # Record deployment report as DEPLOY_BLOCKED
            _record_deploy_blocked(target_live, dist_sha, str(pe))
            return 2
        except Exception as eBak:
            print(f"[ERROR] Failed to create backup copy: {eBak}")
            return 1
    else:
        print("[5/11] No prior file to backup.")

    # Step 6: Perform installation to Live AE
    try:
        os.makedirs(live_dir, exist_ok=True)
        shutil.copy2(dist_file, target_live)
        print(f"[6/11] Copied source artifact to Live target: {target_live}")
    except PermissionError as pe:
        print(f"[FATAL] Permission denied installing to {target_live}: {pe}")
        print("Administrator elevation required. Run scripts/install_admin.cmd as Administrator.")
        _record_deploy_blocked(target_live, dist_sha, str(pe))
        return 2
    except Exception as eCopy:
        print(f"[FATAL] Copy failed: {eCopy}")
        return 1

    # Step 7: Verify new Live hash
    live_sha = compute_sha256(target_live)
    if live_sha != dist_sha:
        print(f"[ERROR] Live file SHA-256 mismatch! Expected {dist_sha}, got {live_sha}")
        return 1
    print(f"[7/11] Live installation verified: SHA-256 = {live_sha}")

    # Step 8: Update Backup Mirror
    target_mirror = os.path.join(MIRROR_INSTALL_DIR, DIST_FILENAME)
    mirror_parent = os.path.dirname(target_mirror)
    try:
        os.makedirs(mirror_parent, exist_ok=True)
        if os.path.exists(target_mirror):
            shutil.copy2(target_mirror, target_mirror + ".bak")
        shutil.copy2(dist_file, target_mirror)
        print(f"[8/11] Synchronized to Backup Mirror: {target_mirror}")
    except Exception as eMirror:
        print(f"[ERROR] Failed to update Backup Mirror: {eMirror}")
        return 1

    # Step 9: Verify Backup Mirror hash
    mirror_sha = compute_sha256(target_mirror)
    if mirror_sha != dist_sha:
        print(f"[ERROR] Backup Mirror SHA-256 mismatch! Expected {dist_sha}, got {mirror_sha}")
        return 1
    print(f"[9/11] Backup Mirror verified: SHA-256 = {mirror_sha}")

    # Step 10: Write deployment report
    deploy_results = {
        "state": DeploymentState.LIVE_AND_MIRROR_VERIFIED,
        "live_installed": True,
        "mirror_installed": True,
        "hashes_match": True,
        "live_path": target_live,
        "mirror_path": target_mirror,
        "live_sha256": live_sha,
        "mirror_sha256": mirror_sha,
        "live_error": None,
        "mirror_error": None,
        "installed_instances": find_installed_instances()
    }
    log_dir = os.path.join(WORKSPACE_ROOT, "logs")
    os.makedirs(log_dir, exist_ok=True)
    report_path = os.path.join(log_dir, "deployment_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(deploy_results, f, indent=2)
    print(f"[10/11] Deployment report written to: {report_path}")

    # Step 11: Final success confirmation
    print(f"[11/11] Installation completed successfully!")
    print(f"        DIST_SHA256:   {dist_sha}")
    print(f"        LIVE_SHA256:   {live_sha}")
    print(f"        MIRROR_SHA256: {mirror_sha}")
    print("ALL THREE ARTIFACTS ARE BYTE-IDENTICAL.")
    return 0

if __name__ == "__main__":
    sys.exit(install_live_and_mirror())
