#!/bin/bash

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️ Error: .env file not found!"
    echo "Please copy .env.example to .env and add your API key."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import paho.mqtt.client, dotenv" 2>/dev/null; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

echo "📡 Starting TermChat MQTT AI Service..."
python3 mqtt_service.py