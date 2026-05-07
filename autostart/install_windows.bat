@echo off
REM Windows autostart installation script for PC Remote Bot

echo ========================================
echo PC Remote Bot - Windows Autostart Setup
echo ========================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
set BOT_DIR=%SCRIPT_DIR%..

echo Bot directory: %BOT_DIR%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install dependencies
echo Installing dependencies...
cd /d "%BOT_DIR%"
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Create .env file if it doesn't exist
if not exist "%BOT_DIR%\.env" (
    echo Creating .env file...
    copy "%BOT_DIR%\.env.example" "%BOT_DIR%\.env"
    echo.
    echo IMPORTANT: Please edit .env file and add your credentials:
    echo - TELEGRAM_BOT_TOKEN
    echo - ADMIN_ID
    echo - DEEPSEEK_API_KEY
    echo.
    notepad "%BOT_DIR%\.env"
)

REM Create startup batch file
echo Creating startup script...
set STARTUP_SCRIPT=%BOT_DIR%\start_bot.bat

echo @echo off > "%STARTUP_SCRIPT%"
echo cd /d "%BOT_DIR%" >> "%STARTUP_SCRIPT%"
echo python main.py >> "%STARTUP_SCRIPT%"

echo Startup script created: %STARTUP_SCRIPT%
echo.

REM Add to Windows startup folder
echo Adding to Windows startup...
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT=%STARTUP_FOLDER%\PC_Remote_Bot.bat

copy "%STARTUP_SCRIPT%" "%SHORTCUT%"

if exist "%SHORTCUT%" (
    echo.
    echo ========================================
    echo Installation completed successfully!
    echo ========================================
    echo.
    echo The bot will now start automatically when Windows starts.
    echo.
    echo To start the bot now, run: start_bot.bat
    echo To remove from startup, delete: %SHORTCUT%
    echo.
) else (
    echo.
    echo WARNING: Could not add to startup folder
    echo You can manually add start_bot.bat to startup
    echo.
)

pause
