#!/usr/bin/env python3
"""
vac34_AE Management CLI
Provides single-entrypoint commands with strict exit codes:
  - build
  - test
  - validate
  - install
  - verify (Strict nonzero exit on any failure)
  - export (Creates clean standalone distribution zip archive)
  - repair-mirror (restores live AE from backup mirror)
  - uninstall
"""

import os
import sys
import shutil
import hashlib
import subprocess
import zipfile
import tempfile
from datetime import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(WORKSPACE_ROOT, "build")
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
if BUILD_DIR not in sys.path:
    sys.path.insert(0, BUILD_DIR)

def get_live_dir():
    """Lazy discovery of After Effects install directory."""
    try:
        from build.builder import discover_ae_install_dir
        return discover_ae_install_dir()
    except Exception:
        try:
            import importlib.util
            builder_path = os.path.join(BUILD_DIR, "builder.py")
            spec = importlib.util.spec_from_file_location("builder", builder_path)
            if spec and spec.loader:
                builder = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(builder)
                return builder.discover_ae_install_dir()
        except Exception:
            pass
    return r"C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels"

LIVE_DIR = None  # Will be resolved lazily on first access

def get_live_path():
    global LIVE_DIR
    if LIVE_DIR is None:
        LIVE_DIR = get_live_dir()
    return os.path.join(LIVE_DIR, "vac34_AE.jsx")

LIVE_PATH = None  # Resolved via get_live_path()
MIRROR_PATH = r"V:\__STORE_V\_AE\install_AEPlugins\_install_healing\Program Files\Adobe\Adobe After Effects 2024\Support Files\Scripts\ScriptUI Panels\vac34_AE.jsx"
DIST_PATH = os.path.join(WORKSPACE_ROOT, "dist", "vac34_AE.jsx")

def sha256_file(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify_vac34_ownership(filepath: str) -> bool:
    """Verifies that a file belongs to vac34 before overwriting or deleting."""
    if not os.path.exists(filepath):
        return True
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            head = f.read(2048)
        return "vac34" in head
    except Exception:
        return False

def cmd_build():
    subprocess.run([sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--no-tests"], check=True)

def cmd_test():
    res = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], cwd=WORKSPACE_ROOT)
    if res.returncode != 0:
        sys.exit(res.returncode)

def cmd_validate():
    subprocess.run([sys.executable, os.path.join(WORKSPACE_ROOT, "build", "ingest_bibles.py")], check=True)
    temp_syntax = os.path.join(WORKSPACE_ROOT, "dist", ".syntax_check.tmp.js")
    shutil.copy2(DIST_PATH, temp_syntax)
    try:
        subprocess.run(["node", "--check", temp_syntax], check=True)
    finally:
        if os.path.exists(temp_syntax):
            os.remove(temp_syntax)
    print("All validation checks PASSED.")

def cmd_install():
    res = subprocess.run([sys.executable, os.path.join(WORKSPACE_ROOT, "build", "builder.py"), "--deploy"])
    if res.returncode != 0:
        sys.exit(res.returncode)

def cmd_verify():
    live_path = get_live_path()
    live_sha = sha256_file(live_path)
    mirror_sha = sha256_file(MIRROR_PATH)
    dist_sha = sha256_file(DIST_PATH)

    print("--- DEPLOYMENT VERIFICATION ---")
    print(f"Dist Artifact:   {DIST_PATH} -> {dist_sha}")
    print(f"Live AE Panel:   {live_path} -> {live_sha}")
    print(f"Backup Mirror:   {MIRROR_PATH} -> {mirror_sha}")

    if live_sha and mirror_sha and dist_sha and (live_sha == mirror_sha == dist_sha):
        print("\n[VERIFIED] All artifacts exist and are byte-identical (SHA-256 match).")
        return True
    elif mirror_sha and dist_sha and mirror_sha == dist_sha:
        print("\n[DEPLOY_BLOCKED] Dist and Backup Mirror are byte-identical, but Live AE Panel is not updated.")
        live_exists = os.path.exists(live_path)
        if live_exists:
            # Check actual write permission vs just content difference
            try:
                with open(live_path, 'a') as f:
                    pass
                write_permitted = True
            except PermissionError:
                write_permitted = False
            print(f"Live AE Panel differs ({str(live_sha)[:8]}... vs {str(dist_sha)[:8]}...)")
            if not write_permitted:
                print("Access denied: target directory is write-protected.")
            else:
                print("Content mismatch: file exists but differs from dist/mirror.")
        else:
            print("Live AE Panel does not exist at target location.")
        print("To update Live AE:")
        print("  1. Run 'scripts\\install_admin.cmd' as Administrator, OR")
        print("  2. In an elevated Administrator terminal run: python scripts/manage.py repair-mirror")
        sys.exit(1)
    else:
        print("\n[DEPLOY_FAILED] Mismatch or missing file detected.")
        sys.exit(1)

def cmd_export():
    print("Executing 10-step Project Release & Export Procedure...")

    # Step 1: Build
    print("[1/10] Building project bundle...")
    cmd_build()

    # Step 2: Test
    print("[2/10] Executing test suite...")
    cmd_test()

    # Step 3: Validate manifest & required artifacts
    print("[3/10] Verifying release contract artifacts...")
    required_files = [
        "build/builder.py",
        "build/ingest_bibles.py",
        "dist/vac34_AE.jsx",
        "release/build_manifest.json",
        "release/vac34_AE_v0.0.1.jsx"
    ]
    missing = [f for f in required_files if not os.path.exists(os.path.join(WORKSPACE_ROOT, f))]
    if missing:
        print(f"[EXPORT ERROR] Missing required build/release artifacts before export: {missing}")
        sys.exit(1)

    # Step 4: Create self-contained ZIP
    print("[4/10] Packaging self-contained distribution archive...")
    export_dir = os.path.join(WORKSPACE_ROOT, "dist")
    os.makedirs(export_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(export_dir, f"vac34_ae_export_{timestamp}.zip")

    include_dirs = ["src", "sources", "catalog", "bibles", "build", "scripts", "tests", "docs", "dist", "release"]
    include_files = ["README.md", "VERSION", ".gitattributes", ".gitignore"]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in include_files:
            p = os.path.join(WORKSPACE_ROOT, f)
            if os.path.exists(p):
                z.write(p, f)
        for d in include_dirs:
            dp = os.path.join(WORKSPACE_ROOT, d)
            if os.path.exists(dp):
                for root, _, files in os.walk(dp):
                    for file in files:
                        fp = os.path.join(root, file)
                        if fp == zip_path or file.endswith(".zip"):
                            continue
                        rel = os.path.relpath(fp, WORKSPACE_ROOT)
                        z.write(fp, rel)

    archive_size = os.path.getsize(zip_path)
    print(f"  Archive created: {zip_path} ({archive_size} bytes)")

    # Step 5: Extract to clean temporary directory
    print("[5/10] Extracting to clean isolated temporary workspace...")
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp_dir)

        # Step 6: Rebuild from extracted source
        print("[6/10] Rebuilding from extracted source in clean environment...")
        rebuild_proc = subprocess.run(
            [sys.executable, os.path.join(temp_dir, "build", "builder.py")],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        if rebuild_proc.returncode != 0:
            print(f"[EXPORT ERROR] Rebuild failed in extracted archive:\n{rebuild_proc.stderr}\n{rebuild_proc.stdout}")
            sys.exit(1)

        # Step 7: Execute complete test suite
        print("[7/10] Executing test discovery on rebuilt extracted workspace...")
        test_res = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        if test_res.returncode != 0:
            print(f"[EXPORT REPRODUCIBILITY ERROR] Tests failed in unpacked archive:\n{test_res.stderr}\n{test_res.stdout}")
            sys.exit(1)

        # Step 8: Verify manifest and expected artifacts in clean workspace
        print("[8/10] Verifying manifest and built artifacts in extracted workspace...")
        temp_dist = os.path.join(temp_dir, "dist", "vac34_AE.jsx")
        temp_manifest = os.path.join(temp_dir, "release", "build_manifest.json")
        if not os.path.exists(temp_dist) or not os.path.exists(temp_manifest):
            print("[EXPORT ERROR] Extracted workspace missing dist or manifest after rebuild.")
            sys.exit(1)

        # Step 9: Compare artifact fingerprints
        print("[9/10] Comparing expected artifact fingerprints...")
        source_sha = sha256_file(DIST_PATH)
        rebuilt_sha = sha256_file(temp_dist)
        if source_sha != rebuilt_sha:
            print(f"[EXPORT ERROR] Artifact SHA-256 fingerprint mismatch between root ({source_sha}) and rebuilt ({rebuilt_sha})")
            sys.exit(1)

        # Step 10: Definitive pass report
        print("[10/10] Definitive verification complete: PASS.")

    print(f"[EXPORT VERIFIED] 100% self-contained reproducible release archive verified clean: {zip_path}")
    return zip_path

def cmd_repair_mirror():
    live_path = get_live_path()
    print("Repairing Live AE from verified Backup Mirror...")
    if not os.path.exists(MIRROR_PATH):
        raise FileNotFoundError(f"Backup mirror not found: {MIRROR_PATH}")
    if not verify_vac34_ownership(MIRROR_PATH):
        raise ValueError(f"Backup mirror is not a valid vac34 product: {MIRROR_PATH}")
    if os.path.exists(live_path):
        if not verify_vac34_ownership(live_path):
            raise PermissionError(f"Target {live_path} does not appear to be a vac34 file; refusing to overwrite foreign file.")
        bak = live_path + ".bak"
        try:
            shutil.copy2(live_path, bak)
            print(f"Backed up current Live to {bak}")
        except Exception as be:
            print(f"Warning: could not backup live: {be}")
    try:
        shutil.copy2(MIRROR_PATH, live_path)
        print(f"Successfully copied {MIRROR_PATH} -> {live_path}")
    except PermissionError as pe:
        print(f"\n[ERROR] Permission denied copying to {live_path}: {pe}")
        print("Please run this command in an elevated Administrator prompt:")
        print("  python scripts/manage.py repair-mirror")
        sys.exit(2)
    cmd_verify()

def cmd_uninstall():
    print("Uninstalling vac34_AE panel from Live AE and Mirror...")
    live_path = get_live_path()
    for target in (live_path, MIRROR_PATH):
        if os.path.exists(target):
            if not verify_vac34_ownership(target):
                print(f"[REJECTED] Target {target} does not match vac34 signature; refusing to delete unknown file.")
                continue
            bak = target + ".bak"
            try:
                shutil.copy2(target, bak)
                print(f"Backed up to {bak} before removal.")
            except Exception:
                pass
            try:
                os.remove(target)
                print(f"Removed: {target}")
            except PermissionError as pe:
                print(f"[PERMISSION ERROR] Cannot remove {target}: {pe} (run as Administrator)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/manage.py [build|test|validate|install|verify|export|repair-mirror|uninstall]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "build":
        cmd_build()
    elif cmd == "test":
        cmd_test()
    elif cmd == "validate":
        cmd_validate()
    elif cmd == "install":
        cmd_install()
    elif cmd == "verify":
        if not cmd_verify():
            sys.exit(1)
    elif cmd == "export":
        cmd_export()
    elif cmd == "repair-mirror":
        cmd_repair_mirror()
    elif cmd == "uninstall":
        cmd_uninstall()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
