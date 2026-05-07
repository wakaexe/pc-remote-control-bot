@echo off
REM Quick start script for PC Remote Bot
echo Starting PC Remote Bot...
echo.

cd /d "%~dp0"

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

REM Start bot
python main.py

pause
