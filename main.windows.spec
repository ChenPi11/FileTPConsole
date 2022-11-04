# -*- mode: python ; coding: utf-8 -*-

import compileall
import os
import glob
import shutil

block_cipher = None

a = Analysis(['main.windows.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=["subprocess"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=["PyQt5","PySide2","PySide6","tcl","tkinter","QtPy","numpy","pygame"],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main.windows',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon=['./res/icon.ico'],
          version='./res/main.windows.spec.version.txt' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FileTPConsole')
print("clean filetp/__pycache__ ...")
shutil.rmtree("./filetp/__pycache__")
print("copying filetp files...")
compileall.compile_dir("./filetp/")
print("compiled")
distdir="./dist/FileTPConsole/"
os.makedirs(distdir+"filetp")
print("mkdir:",distdir+"filetp")
for i in glob.glob("./filetp/__pycache__/*.pyc"):
	name=""
	try:
		name=i.split(".")[0]+".pyc"
	except:
		name=i
	os.rename(i,name)
shutil.copytree("./filetp",distdir+"filetp")
print("copied!")
