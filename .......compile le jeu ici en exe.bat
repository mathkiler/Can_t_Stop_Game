@echo off

pyinstaller --noconfirm --onefile --windowed --icon "./assets/images/icon.ico" --add-data "./assets;assets/"  "./Cant_Stop_Game.py"
rmdir /q /s build
del "Cant_Stop_Game.spec"
cd ".\dist"
move "Cant_Stop_Game.exe" ..
cd ".."
rmdir /q /s dist