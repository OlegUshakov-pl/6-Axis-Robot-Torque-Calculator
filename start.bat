@echo off
cd /d "%~dp0"

if not exist "..\venv\Scripts\streamlit.exe" (
    echo Virtual environment not found.
    echo Run install.bat first.
    pause
    exit /b 1
)

echo Starting Manipulator Torque Calculator...
call ..\venv\Scripts\streamlit.exe run app.py
pause
