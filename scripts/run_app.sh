#!/usr/bin/env bash

set -e

APP_DIR="/home/ec2-user/flask-chatbot/personal-chatbot"
VENV_PATH="$APP_DIR/venv_app/bin"
GUNICORN_EXECUTABLE="$VENV_PATH/gunicorn"

cd "$APP_DIR"

echo "Fetching parameters from Systems Manager..."

export GCP_LOCATION=$(aws ssm get-parameter --name "/GCP_LOCATION" --query "Parameter.Value" --output text)
export GCP_PROJECT_ID=$(aws ssm get-parameter --name "/GCP_PROJECT_ID" --query "Parameter.Value" --output text)
export GEMINI_MODEL=$(aws ssm get-parameter --name "/GEMINI_MODEL" --query "Parameter.Value" --output text)

SECRET_RESPONSE=$(aws secretsmanager get-secret-value \
    --secret-id "GoogleCredentials" \
    --output json)

CREDENTIALS_JSON=$(echo "$SECRET_RESPONSE" | jq -r '.SecretString')
CREDENTIALS_FILE="$APP_DIR/credentials.json"

cat <<EOF > "$CREDENTIALS_FILE"
$CREDENTIALS_JSON
EOF

chmod 600 "$CREDENTIALS_FILE"

export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_FILE"

echo "Starting Gunicorn..."
exec $GUNICORN_EXECUTABLE -b 0.0.0.0:8086 app.main:APP --workers=1 --threads=2 --timeout=120