#!/bin/bash

echo "========================================"
echo "PC Remote Bot - Client Installer (Linux/Mac)"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3.11+ first"
    exit 1
fi

echo "[OK] Python is installed"
echo ""

# Get token from user
read -p "Enter your PC token from Telegram bot: " TOKEN
if [ -z "$TOKEN" ]; then
    echo "[ERROR] Token cannot be empty!"
    exit 1
fi

# Get PC name
read -p "Enter a name for this PC (optional): " PC_NAME

# Get WebSocket server URL
read -p "Enter WebSocket server URL (default: ws://localhost:8765): " WS_URL
WS_URL=${WS_URL:-ws://localhost:8765}

echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi

echo ""
echo "Creating configuration file..."
cat > .env << EOF
WS_SERVER_URL=$WS_URL
PC_CLIENT_TOKEN=$TOKEN
EOF

echo ""
echo "[OK] Installation complete!"
echo ""
echo "To start the client, run: python3 pc_client.py"
echo ""

# Ask if user wants to add to startup (systemd for Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    read -p "Add to system startup (systemd)? (y/n): " STARTUP
    if [[ "$STARTUP" == "y" || "$STARTUP" == "Y" ]]; then
        echo ""
        echo "Creating systemd service..."

        CURRENT_DIR=$(pwd)

        sudo tee /etc/systemd/system/pc-remote-client.service > /dev/null << EOF
[Unit]
Description=PC Remote Bot Client
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/python3 $CURRENT_DIR/pc_client.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        sudo systemctl daemon-reload
        sudo systemctl enable pc-remote-client.service
        sudo systemctl start pc-remote-client.service

        echo "[OK] Service installed and started!"
        echo "Check status with: sudo systemctl status pc-remote-client"
    fi
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Run: python3 pc_client.py"
echo "2. Check Telegram bot with /mypcs"
echo ""
