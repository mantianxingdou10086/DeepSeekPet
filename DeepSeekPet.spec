# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pet.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/rice', 'assets/rice'), ('assets/layered', 'assets/layered'), ('assets/happy', 'assets/happy'), ('assets/typing', 'assets/typing'), ('assets/prone', 'assets/prone'), ('assets/wakeup', 'assets/wakeup'), ('pet.ico', '.')],
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
    [],
    exclude_binaries=True,
    name='DeepSeekPet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=['pet.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DeepSeekPet',
)
