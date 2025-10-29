#!/bin/bash
export PATH=$PATH:/usr/local/bin:/usr/bin

cd /home/ec2-user/flask-chatbot/personal-chatbot

export GCP_LOCATION=$(aws ssm get-parameter --name "/GCP_LOCATION" --query "Parameter.Value" --output text)
export GCP_PROJECT_ID=$(aws ssm get-parameter --name "/GCP_PROJECT_ID" --query "Parameter.Value" --output text)
export GEMINI_MODEL=$(aws ssm get-parameter --name "/GEMINI_MODEL" --query "Parameter.Value" --output text)

CREDENTIALS_JSON=$(aws ssm get-parameter --name "/GOOGLE_APPLICATION_CREDENTIALS" --query "Parameter.Value" --output text)
CREDENTIALS_FILE="/home/ec2-user/flask-chatbot/personal-chatbot/credentials.json"
echo "$CREDENTIALS_JSON" > "$CREDENTIALS_FILE"
export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_FILE"

exec /usr/local/bin/gunicorn -b 0.0.0.0:8086 app.main:APP --workers=1 --threads=2 --timeout=120