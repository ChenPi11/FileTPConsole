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
             hiddenimports=["subprocess","qrcode"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
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
print(os.path.abspath("."))
print("clean filetp/__pycache__ ...")
try:
	shutil.rmtree("./filetp/__pycache__")
except:
	pass
print("copying filetp files...")
compileall.compile_dir("./filetp/")
print("compiled")
distdir="./dist/FileTPConsole/"
for i in glob.glob("./filetp/__pycache__/*.pyc"):
	name=""
	try:
		name="."+i.split(".")[1]+".pyc"
	except:
		name=i
	print("rename:",i,"to",name,"...")
	os.rename(i,name)
shutil.copytree("./filetp/__pycache__",distdir+"filetp")
print("copied!")
