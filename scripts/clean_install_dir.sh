#!/bin/bash
set -ex

TARGET_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"

if [ -d "$TARGET_DIR" ]; then
    sudo rm -rf "$TARGET_DIR"/*
    sudo rm -rf "$TARGET_DIR"/.* 
else
    sudo mkdir -p "$TARGET_DIR"
fi