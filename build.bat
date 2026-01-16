@echo off
echo Building Child Growth Analyzer...
python -m PyInstaller --noconfirm --onefile --windowed --name "CocukGelisimTakip" --clean "main.py"
echo Build Finished! Exe file is in the dist folder.
pause
