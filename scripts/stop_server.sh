#!/bin/bash
sudo systemctl stop flaskapp || true
sudo systemctl disable flaskapp || true

PID=$(lsof -t -i:8086)

if [ -n "$PID" ]; then
    echo "Found rogue process on port 8086 (PID: $PID). Killing process..."
    sudo kill -9 $PID || true
    sleep 2
    echo "Process killed."
else
    echo "No rogue processes found on port 8086."
fi

exit 0