#!/usr/bin/env bash
systemctl stop flaskapp 2>/dev/null || true
systemctl disable flaskapp 2>/dev/null || true

PID=$(lsof -t -i:8086 2>/dev/null)

if [ -n "$PID" ]; then
    echo "Found rogue process on port 8086 (PID: $PID). Killing process..."
    kill -9 $PID 2>/dev/null || true
    sleep 2
    echo "Process killed."
else
    echo "No rogue processes found on port 8086."
fi

# 腳本正常結束，確保返回碼為 0
exit 0