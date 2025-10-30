#!/bin/bash
set -ex

systemctl stop flaskapp  || true
systemctl disable flaskapp || true

PID=$(lsof  -t -i:8086 2>/dev/null)

if [ -n "$PID" ]; then
    echo "Found rogue process on port 8086 (PID: $PID). Killing process..."
    kill -9 $PID 2 || true
    sleep 2
    echo "Process killed."
else
    echo "No rogue processes found on port 8086."
fi

TARGET_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"

if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"/*
else
    sudo mkdir -p "$TARGET_DIR"
fi

exit 0