# -*- mode: python -*-

block_cipher = None


a = Analysis(['StructureTemplateManager.py'],
             pathex=["C:\\Users\\gsalomon\\OneDrive - Queen's University\\Python\\Projects\\EclipseRelated\\Manage Templates\\ManageStructuresTemplates"],
             binaries=[],
             datas=[('StructuresGUI.xml', '.'), ('.\\icons\\Box2.png', 'icons'), ('.\\icons\\Blueprint2.png', 'icons'), ('.\\icons\\DVH Black smaller.png', 'icons'), ('.\\icons\\DVH2.ico', 'icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt5'],
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
          name='StructureTemplateManager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icons\\DVH2.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='StructureTemplateManager')
