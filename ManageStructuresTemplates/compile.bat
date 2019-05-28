pyinstaller --noconfirm --log-level=WARN ^
    --onedir --nowindow ^
    --add-data="StructuresGUI.xml;." ^
    --add-data=".\icons\Box2.png;icons" ^
    --add-data=".\icons\Blueprint2.png;icons" ^
    --add-data=".\icons\DVH Black smaller.png;icons" ^
    --add-data=".\icons\DVH2.ico;icons" ^
    --icon=.\icons\DVH2.ico ^
    --exclude-module PyQt5 ^
    StructureTemplateManager.py


