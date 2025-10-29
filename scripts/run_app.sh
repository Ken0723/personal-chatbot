#!/bin/bash
set -e

APP_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"
VENV_PATH="$APP_DIR/venv_app/bin"
GUNICORN_EXECUTABLE="$VENV_PATH/gunicorn"

cd "$APP_DIR"

echo "Fetching parameters from Systems Manager..."

export GCP_LOCATION=$(aws ssm get-parameter --name "/GCP_LOCATION" --query "Parameter.Value" --output text)
export GCP_PROJECT_ID=$(aws ssm get-parameter --name "/GCP_PROJECT_ID" --query "Parameter.Value" --output text)
export GEMINI_MODEL=$(aws ssm get-parameter --name "/GEMINI_MODEL" --query "Parameter.Value" --output text)

CREDENTIALS_JSON=$(aws secretsmanager get-secret-value \
    --secret-id "/GOOGLE_APPLICATION_CREDENTIALS" \
    --query "SecretString" \
    --output text)

CREDENTIALS_FILE="$APP_DIR/credentials.json"

echo "$CREDENTIALS_JSON" > "$CREDENTIALS_FILE"
chmod 600 "$CREDENTIALS_FILE"

export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_FILE"

echo "Starting Gunicorn..."
exec $GUNICORN_EXECUTABLE -b 0.0.0.0:8086 app.main:APP --workers=1 --threads=2 --timeout=120