#!/bin/bash

set -e

# ----------------------------------------
# Configuration
# ----------------------------------------
CONFIG_DIR="/etc/memomart"
CONFIG_FILE="$CONFIG_DIR/memomart.env"
INSTALL_DIR="/opt/memomart"

# ----------------------------------------
# Require root
# ----------------------------------------

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo:"
    echo
    echo "    sudo ./setup.sh"
    echo
    exit 1
fi

echo "================================"
echo " Mem-O-Mart Setup"
echo "================================"
echo

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Project directory:"
echo "  $PROJECT_DIR"
echo

# ----------------------------------------
# Installing Docker
# ----------------------------------------
if command -v docker >/dev/null 2>&1; then
    echo "Docker already installed."
else
    echo "Installing Docker..."

    curl -fsSL https://get.docker.com | sh
fi

systemctl enable docker
systemctl start docker

if docker compose version >/dev/null 2>&1; then
    echo "Docker Compose available."
else
    echo "Error: Docker Compose is not available."
    exit 1
fi

# ----------------------------------------
# Create environment configuration file
# '.env' in /etc/memomart
# ----------------------------------------
echo "Creating environment configuration file..."
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"
if [ -f "$CONFIG_FILE" ]; then
    echo "Environment configuration file already exists: $CONFIG_FILE"
else
    echo "Creating new environment configuration file: $CONFIG_FILE"
    SECRET_KEY="$(openssl rand -hex 32)"
    cat > "$CONFIG_FILE" << EOF
FM_SECRET_KEY=$SECRET_KEY
EOF
    chown root:docker "$CONFIG_FILE"
    chmod 640 "$CONFIG_FILE"
    echo "Configuration created."
fi

# ----------------------------------------
# Install the application to the correct
# directory
# ----------------------------------------
echo "Installing Mem-O-Mart to $INSTALL_DIR..."

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -a "$PROJECT_DIR/." "$INSTALL_DIR/"
cd "$INSTALL_DIR"

# ----------------------------------------
# Build docker image
# ----------------------------------------
echo
echo "Building Docker image..."
echo
docker compose build

cat > "$CONFIG_FILE" << EOF
FM_SECRET_KEY=$SECRET_KEY
EOF
chown root:docker "$CONFIG_FILE"
chmod 640 "$CONFIG_FILE"

# ----------------------------------------
# Create the systemd service
# ----------------------------------------
cat > /etc/systemd/system/memomart.service << EOF
[Unit]
Description=Mem-O-Mart Photobooth
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable memomart.service
systemctl start memomart.service

echo
echo "Checking Mem-O-Mart..."
echo

systemctl status memomart.service --no-pager
docker compose ps

echo
echo "================================"
echo " Setup complete!"
echo "================================"
echo
echo "Mem-O-Mart is installed at:"
echo "  $INSTALL_DIR"
echo
echo "Configuration:"
echo "  $CONFIG_FILE"
echo
echo "Useful commands:"
echo "  sudo systemctl status memomart"
echo "  sudo systemctl restart memomart"
echo "  docker compose -f $INSTALL_DIR/compose.yaml logs -f"
echo