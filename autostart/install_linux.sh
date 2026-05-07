#!/bin/bash
# Linux autostart installation script for PC Remote Bot

echo "========================================"
echo "PC Remote Bot - Linux Autostart Setup"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Bot directory: $BOT_DIR"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ using your package manager"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing dependencies..."
cd "$BOT_DIR"
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Dependencies installed successfully!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f "$BOT_DIR/.env" ]; then
    echo "Creating .env file..."
    cp "$BOT_DIR/.env.example" "$BOT_DIR/.env"
    echo ""
    echo "IMPORTANT: Please edit .env file and add your credentials:"
    echo "- TELEGRAM_BOT_TOKEN"
    echo "- ADMIN_ID"
    echo "- DEEPSEEK_API_KEY"
    echo ""
    echo "Opening .env file in editor..."
    ${EDITOR:-nano} "$BOT_DIR/.env"
fi

# Create systemd service
echo "Creating systemd service..."

SERVICE_FILE="/etc/systemd/system/pc-remote-bot.service"

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=PC Remote Control Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_DIR
Environment="PATH=$PATH"
ExecStart=$(which python3) $BOT_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

if [ $? -eq 0 ]; then
    echo "Service file created: $SERVICE_FILE"
    echo ""

    # Reload systemd
    echo "Reloading systemd..."
    sudo systemctl daemon-reload

    # Enable service
    echo "Enabling service..."
    sudo systemctl enable pc-remote-bot.service

    # Start service
    echo "Starting service..."
    sudo systemctl start pc-remote-bot.service

    echo ""
    echo "========================================"
    echo "Installation completed successfully!"
    echo "========================================"
    echo ""
    echo "Service commands:"
    echo "  Start:   sudo systemctl start pc-remote-bot"
    echo "  Stop:    sudo systemctl stop pc-remote-bot"
    echo "  Restart: sudo systemctl restart pc-remote-bot"
    echo "  Status:  sudo systemctl status pc-remote-bot"
    echo "  Logs:    sudo journalctl -u pc-remote-bot -f"
    echo ""
    echo "The bot will now start automatically on system boot."
    echo ""
else
    echo ""
    echo "ERROR: Failed to create systemd service"
    echo "You may need to run this script with sudo"
    exit 1
fi
