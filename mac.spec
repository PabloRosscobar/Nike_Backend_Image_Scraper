# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=['json', 'requests.exceptions', 'colorama', 'requests', 'PySimpleGUI', 'urllib3', 'sys', 'time', 
             'os', 'datetime', 'Scraper', 'string', 'sys', 'colorlog', 'Tools',
             ],
             hookspath=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='NIKE IMAGE SCRAPER',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='')
