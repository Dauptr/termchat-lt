# termAi/chat_interface.py
import time
from .models import SimpleChatBot

class VirtualUser:
    def __init__(self, name="TermAi"):
        self.name = name
        # Initialize the "brain"
        self.brain = SimpleChatBot(vocab_size=10)
        print(f"[System] Virtual User '{self.name}' has joined the chat.")

    def on_receive_message(self, message, sender_name):
        """
        This function is called by TermChat LT whenever a user types something.
        """
        print(f"{sender_name}: {message}")
        
        # Simulate "thinking" time (latency)
        time.sleep(1)
        
        # 1. Process the message using the termAi library
        response_text = self.brain.think(message)
        
        # 2. Send the response back to the chat
        return response_text

# --- Example Simulation of TermChat LT ---
if __name__ == "__main__":
    # Create the AI User
    ai_user = VirtualUser("TermAi")
    
    print("--- TermChat LT Simulation Started ---")
    
    # Simulate a user talking
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
            
        # The Chat App calls the AI
        ai_reply = ai_user.on_receive_message(user_input, "You")
        print(f"{ai_user.name}: {ai_reply}")