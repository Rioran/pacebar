@echo off
REM Double-click to build a slimmed-down standalone exe into dist\ (Windows).
cd /d "%~dp0\.."
uv run --extra build pyinstaller --noconfirm --clean pacebar.spec
echo.
echo Built: dist\pacebar.exe
pause
