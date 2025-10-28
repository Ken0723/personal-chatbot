#!/bin/bash

APP_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"
SERVICE_FILE="/scripts/flaskapp.service"

echo "Stopping existing Flask service..."
systemctl stop flaskapp || true

echo "Copying new Systemd service file..."
cp "$APP_DIR/$SERVICE_FILE" /etc/systemd/system/$SERVICE_FILE

echo "Setting permissions..."
chown -R ec2-user:ec2-user "$APP_DIR"

echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling and starting Flask service..."
systemctl enable flaskapp
systemctl start flaskapp

echo "Status check..."
systemctl status flaskapp