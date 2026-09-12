@echo off
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3.14"
) else (
    set "PYTHON_CMD=python"
)

echo Creating virtual environment in parent folder...
%PYTHON_CMD% -m venv ..\venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

if exist "..\venv\Scripts\python.exe" (
    set "VENV_PYTHON=..\venv\Scripts\python.exe"
) else (
    set "VENV_PYTHON=..\venv\bin\python.exe"
)

echo Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

set "SCRIPT_DIR=%~dp0"

echo Installing dependencies...
%VENV_PYTHON% -m pip install --prefer-binary -r "%SCRIPT_DIR%requirements.txt"
if %errorlevel% neq 0 (
    echo.
    echo Retrying with trusted hosts...
    %VENV_PYTHON% -m pip install --prefer-binary --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "%SCRIPT_DIR%requirements.txt"
)
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Check your internet connection or SSL certificates.
    pause
    exit /b 1
)

echo.
echo Installation complete! Run start.bat to launch the app.
pause