# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(2000)


block_cipher = None


a = Analysis(
    ['main.py','Gui/__init__.py','data/__init__.py','ctrl/__init__.py','Gui/Login.py','Gui/Login.py','Gui/MainWindow.py','ctrl/compute_slot.py','ctrl/jieliu_slot.py','ctrl/Login_slot.py','ctrl/mappint_slot.py','ctrl/matlab_slot.py','ctrl/menu_slot.py','ctrl/result_slot.py','data/result_form.py','matlab_project/__init__.py'
    ,'matlab_project/BWRSv0.py','matlab_project/BWRSV1.py','matlab_project/BWRSV2.py','matlab_project/G.py','matlab_project/JL3.py','matlab_project/main.py','matlab_project/MAXQd.py','matlab_project/Mz.py','matlab_project/ttf.py'],
    pathex=['Project'],
    binaries=[],
    datas=[('matlab2','matlab2'),('resource','resource'),('ctrl','ctrl'),('F:\\Users\\12875\\anaconda3\\envs\\matlab\\Lib\\site-packages\\matlab','matlab'),('F:\\Users\\12875\\anaconda3\\envs\\matlab\\Lib\\site-packages\\openpyxl','openpyxl'),('F:\\Users\\12875\\anaconda3\\envs\\matlab\\Lib\\site-packages\\matplotlib','matplotlib')],
    hiddenimports=['pkg_resources.extern','matlab.engine','openpyxl','openpyxl.cell._writer','matplotlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
