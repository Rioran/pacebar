# -*- mode: python ; coding: utf-8 -*-
# Standard one-file build. Entry point is entry.py (absolute imports) rather than
# the package __main__, which would build but crash at launch when frozen.

from PyInstaller.utils.hooks import collect_submodules

# pynput loads its platform backend dynamically (importlib), so PyInstaller's
# static analysis misses it. Without these the global hotkeys silently die.
_HIDDEN_IMPORTS = collect_submodules("pynput")

a = Analysis(
    ['entry.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=_HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pacebar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # avoid antivirus false-positives on packed Qt DLLs
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app, no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
