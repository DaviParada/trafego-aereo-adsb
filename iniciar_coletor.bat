@echo off
cd /d "C:\Users\Davi\Desktop\ProjetoEmbraer"
:loop
py coletor.py
echo.
echo Coletor saiu. Reiniciando em 30 segundos...
timeout /t 30
goto loop
