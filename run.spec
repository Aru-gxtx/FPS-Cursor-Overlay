# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\admin\\OneDrive\\Documents\\vs_code\\cursorrg\\run.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['idlelib', 'lib2to3', 'doctest', 'unittest', 'pydoc_data', 'turtledemo', 'tkinter.test', 'tkinter.tix', 'numpy', 'pandas', 'scipy', 'matplotlib', 'IPython', 'jupyter', 'notebook', 'torch', 'tensorflow', 'cv2', 'skimage', 'seaborn'],
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
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
