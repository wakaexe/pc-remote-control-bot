@echo off
echo ========================================
echo PC Remote Bot - Client Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Get token from user
set /p TOKEN="Enter your PC token from Telegram bot: "
if "%TOKEN%"=="" (
    echo [ERROR] Token cannot be empty!
    pause
    exit /b 1
)

REM Get PC name
set /p PC_NAME="Enter a name for this PC (optional): "

REM Get WebSocket server URL
set /p WS_URL="Enter WebSocket server URL (default: ws://localhost:8765): "
if "%WS_URL%"=="" set WS_URL=ws://localhost:8765

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Creating configuration file...
(
echo WS_SERVER_URL=%WS_URL%
echo PC_CLIENT_TOKEN=%TOKEN%
) > .env

echo.
echo [OK] Installation complete!
echo.
echo To start the client, run: python pc_client.py
echo.

REM Ask if user wants to add to startup
set /p STARTUP="Add to Windows startup? (y/n): "
if /i "%STARTUP%"=="y" (
    echo.
    echo Creating startup script...

    REM Get current directory
    set CURRENT_DIR=%CD%

    REM Create startup batch file
    (
        echo @echo off
        echo cd /d "%CURRENT_DIR%"
        echo python pc_client.py
    ) > "%CURRENT_DIR%\start_client.bat"

    REM Copy to startup folder
    copy "%CURRENT_DIR%\start_client.bat" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\" >nul

    echo [OK] Added to startup!
    echo The client will start automatically when Windows starts.
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python pc_client.py
echo 2. Check Telegram bot with /mypcs
echo.
pause
