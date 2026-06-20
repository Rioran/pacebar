@echo off
REM Double-click to build a slimmed-down standalone exe into dist\ (Windows).
cd /d "%~dp0\.."
uv run --extra build pyinstaller --noconfirm --clean meet-control.spec
echo.
echo Built: dist\meet-control.exe
pause
