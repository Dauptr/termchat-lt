#!/bin/bash
# Render build script

echo "Starting TermOS LT build process..."

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installations
python -c "import paho.mqtt.client as mqtt; print('MQTT client OK')"
python -c "import zhipuai; print('Zhipu AI OK')"

echo "Build completed successfully!"