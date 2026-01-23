import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from backend import get_ai_response
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Load Config
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.emqx.io")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "term-chat/global/v3"
AI_USER_ID = os.getenv("AI_USER_ID", "TERMAI")
PORT = int(os.getenv("PORT", 10000))

# Debug logging
print(f"🔧 DEBUG: MQTT_BROKER={MQTT_BROKER}")
print(f"🔧 DEBUG: MQTT_PORT={MQTT_PORT}")
print(f"🔧 DEBUG: AI_USER_ID={AI_USER_ID}")
print(f"🔧 DEBUG: PORT={PORT}")
print(f"🔧 DEBUG: OPENAI_API_KEY={'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")

# HTTP Server for Render health check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        status = {
            "status": "running",
            "service": "TermChat MQTT AI Bot",
            "ai_user_id": AI_USER_ID,
            "mqtt_broker": MQTT_BROKER
        }
        self.wfile.write(json.dumps(status).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

def start_http_server():
    """Start HTTP server for Render port binding"""
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    print(f"🌐 HTTP server started on port {PORT}")
    server.serve_forever()

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

def start_mqtt_client():
    """Start MQTT client in separate thread"""
    # Fix deprecation warning
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"🚀 Starting MQTT connection to {MQTT_BROKER}:{MQTT_PORT}")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"💥 MQTT connection failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting TermChat MQTT AI Service...")
    
    # Start MQTT client in background thread
    mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
    mqtt_thread.start()
    
    # Start HTTP server (blocks main thread)
    start_http_server()