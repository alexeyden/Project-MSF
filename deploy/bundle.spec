# -*- mode: python -*-

import platform
import os
import shutil

ucrt = []
win_sdk = 'C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/x86'

if platform.system() == 'Windows':
	ucrt = [(item, win_sdk + '/' + item) for item in os.listdir(win_sdk)]

block_cipher = None

a = Analysis(['../src/server/server.py'],
             pathex=[
                 '../src/server'
             ],
             binaries=[],
             datas=[('../src/server/data', 'data'), ('../src/client', 'client')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='server',
          debug=False,
          strip=False,
          upx=True,
          console=True, icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='server')

print('Copying UCRT DLLS...')
for item in ucrt:
	shutil.copyfile(item[1], 'dist/server/' + item[0])	
