#!/bin/bash
set -e

APP_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"
SERVICE_FILE="flaskapp.service"

echo "Copying new Systemd service file..."
sudo cp "$APP_DIR/$SERVICE_FILE" /etc/systemd/system/$SERVICE_FILE

echo "Setting permissions..."
sudo chown -R ec2-user:ec2-user "$APP_DIR"

sudo chmod +x "$APP_DIR/scripts/run_app.sh" 

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting Flask service..."
sudo systemctl enable flaskapp
sudo systemctl start flaskapp

echo "Status check..."
sudo systemctl status flaskapp