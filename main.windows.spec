# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.windows.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=["subprocess"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=["PyQt5","PySide2","tcl","tkinter","QtPy","numpy","pygame"],
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