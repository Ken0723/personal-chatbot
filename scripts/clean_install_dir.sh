#!/bin/bash
set -ex

TARGET_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"

if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"/*
    sudo rm -rf "$TARGET_DIR"/.* 
else
    sudo mkdir -p "$TARGET_DIR"
fi

/usr/bin/systemctl stop flaskapp 2>/dev/null || true
/usr/bin/systemctl disable flaskapp 2>/dev/null || true

PID=$(/usr/sbin/lsof -t -i:8086 2>/dev/null)

if [ -n "$PID" ]; then
    echo "Found rogue process on port 8086 (PID: $PID). Killing process..."
    /usr/bin/kill -9 $PID 2>/dev/null || true
    sleep 2
    echo "Process killed."
else
    echo "No rogue processes found on port 8086."
fi

exit 0