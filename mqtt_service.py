import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from backend import get_ai_response

# Load Config
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.emqx.io")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "term-chat/global/v3"
AI_USER_ID = os.getenv("AI_USER_ID", "TERMAI")

# Keep service alive for Render
import time
import threading

def keep_alive():
    """Keep the service running for cloud deployment"""
    while True:
        time.sleep(30)
        print("🔄 Service alive...")

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT Broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        
        # Only respond to chat messages, not AI's own messages
        if payload.get("type") == "chat" and payload.get("id") != AI_USER_ID:
            user_message = payload.get("msg", "")
            sender_id = payload.get("id", "unknown")
            
            # Only respond to questions or mentions of AI
            if ("?" in user_message or 
                "ai" in user_message.lower() or 
                "termai" in user_message.lower()):
                
                print(f"📨 Received from {sender_id}: {user_message}")
                
                # Get response from termAi
                ai_response = get_ai_response(user_message, use_api=False)
                
                # Publish AI response
                response_payload = json.dumps({
                    "type": "chat",
                    "id": AI_USER_ID,
                    "msg": ai_response
                })
                client.publish(MQTT_TOPIC, response_payload)
                print(f"📤 AI responded: {ai_response}")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

# Start the Service
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🚀 Starting TermChat MQTT AI Service...")
print(f"🔗 Connecting to {MQTT_BROKER}:{MQTT_PORT}")
print(f"🤖 AI User ID: {AI_USER_ID}")

# Start keep-alive thread for cloud deployment
keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
keep_alive_thread.start()

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()