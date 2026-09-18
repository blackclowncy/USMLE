@echo off
title MedPulse USMLE Q-Bank - Tactile Neumorphic Suite
color 0b

echo ====================================================================
echo        MEDPULSE USMLE STEP 1 PATHOLOGY REVIEW & QUESTION BANK
echo               (Tactile Warm Neumorphic Architecture)
echo ====================================================================
echo.
echo Select an option:
echo [1] Launch Standalone Q-Bank directly in Default Browser
echo [2] Re-compile Question Database (python build_database.py)
echo [3] Re-generate index.html (python generate_index_html.py)
echo [4] Exit
echo.

set /p choice="Enter choice (1-4) [Default is 1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="1" goto launch_browser
if "%choice%"=="2" goto rebuild_db
if "%choice%"=="3" goto rebuild_html
if "%choice%"=="4" goto end

:launch_browser
echo.
echo Launching MedPulse USMLE Q-Bank in your default browser...
start "" "%~dp0index.html"
goto end

:rebuild_db
echo.
echo Rebuilding questions database from markdown source files...
python "%~dp0build_database.py"
echo Done.
pause
goto end

:rebuild_html
echo.
echo Regenerating index.html...
python "%~dp0generate_index_html.py"
echo Done.
pause
goto end

:end
exit /b
