# -*- mode: python ; coding: utf-8 -*-
# Standard one-file build. Entry point is entry.py (absolute imports) rather than
# the package __main__, which would build but crash at launch when frozen.

a = Analysis(
    ['entry.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='meet-control',
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
