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

# Debug logging
print(f"🔧 DEBUG: MQTT_BROKER={MQTT_BROKER}")
print(f"🔧 DEBUG: MQTT_PORT={MQTT_PORT}")
print(f"🔧 DEBUG: AI_USER_ID={AI_USER_ID}")
print(f"🔧 DEBUG: OPENAI_API_KEY={'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")

# Keep service alive for Render
import time
import threading

def keep_alive():
    """Keep the service running for cloud deployment"""
    while True:
        time.sleep(30)
        print("🔄 Service alive...")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to MQTT Broker successfully!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
        
        # Send join message
        join_msg = json.dumps({
            "type": "join",
            "id": AI_USER_ID,
            "msg": "AI Bot is now online!"
        })
        client.publish(MQTT_TOPIC, join_msg)
        print(f"📢 AI Bot announced presence as {AI_USER_ID}")
    else:
        print(f"❌ Failed to connect to MQTT Broker. Code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📨 Received message: {payload}")
        
        # Only respond to chat messages, not AI's own messages
        if payload.get("type") == "chat" and payload.get("id") != AI_USER_ID:
            user_message = payload.get("msg", "")
            sender_id = payload.get("id", "unknown")
            
            # Only respond to questions or mentions of AI
            if ("?" in user_message or 
                "ai" in user_message.lower() or 
                "termai" in user_message.lower()):
                
                print(f"🤖 Processing message from {sender_id}: {user_message}")
                
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
        import traceback
        traceback.print_exc()

def on_disconnect(client, userdata, rc):
    print(f"⚠️ Disconnected from MQTT Broker. Code: {rc}")

# Start the Service
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("🚀 Starting TermChat MQTT AI Service...")
print(f"🔗 Connecting to {MQTT_BROKER}:{MQTT_PORT}")
print(f"🤖 AI User ID: {AI_USER_ID}")

try:
    # Start keep-alive thread for cloud deployment
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("🔄 Starting MQTT loop...")
    client.loop_forever()
except Exception as e:
    print(f"💥 Fatal error: {e}")
    import traceback
    traceback.print_exc()