@echo off
setlocal enabledelayedexpansion
title vac34_AE Live Panel Elevated Installer

:: Guard against infinite recursion loop
if "%~1"=="--elevated" goto :run_install

:: Robust Administrator check using fltmc (never net session, which fails when Server service is disabled)
fltmc >nul 2>&1
if %errorlevel% equ 0 goto :run_install

echo [REQUESTING ELEVATION] Restarting with Administrator privileges...
powershell -NoProfile -Command "Start-Process cmd.exe -WorkingDirectory '%~dp0..' -ArgumentList '/c ""%~f0" --elevated"' -Verb RunAs"
exit /b

:run_install
cd /d "%~dp0.."
set "SCRIPT_DIR=%~dp0"
set "INSTALL_PY=%SCRIPT_DIR%install_live.py"

echo ========================================================
echo  vac34_AE — Master Expressions Studio Live Installer
echo ========================================================
echo.

set "PY_CMD="
if exist "C:\ProgramData\SAI\SAIPEN\python\3.11.9-64\python.exe" (
    set "PY_CMD=C:\ProgramData\SAI\SAIPEN\python\3.11.9-64\python.exe"
) else (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_CMD=python"
    ) else (
        where py >nul 2>&1
        if !errorlevel! equ 0 (
            set "PY_CMD=py"
        )
    )
)

if not defined PY_CMD (
    echo [ERROR] Python not found on system. Please install Python 3.
    set "EXIT_CODE=1"
    goto :finish
)

"%PY_CMD%" "%INSTALL_PY%"
set "EXIT_CODE=!errorlevel!"

:finish

if !EXIT_CODE! equ 0 (
    echo.
    echo [SUCCESS] Elevated installation completed and verified!
) else (
    echo.
    echo [ERROR] Installation failed with exit code !EXIT_CODE!.
)

echo.
echo Press any key to close this window.
pause >nul
exit /b !EXIT_CODE!
