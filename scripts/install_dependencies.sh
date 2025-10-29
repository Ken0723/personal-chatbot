#!/bin/bash
set -ex

APP_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"

sudo yum update -y
sudo yum install python3 python3-pip jq -y 

cd $APP_DIR
if [ ! -d "venv_app" ]; then
    python3 -m venv venv_app
fi

source venv_app/bin/activate 

pip install --upgrade pip
pip install -r requirements.txt

deactivate
echo "Dependencies installed successfully in venv_app."