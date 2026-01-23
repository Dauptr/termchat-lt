import json
import os

class ChatLogger:
    def __init__(self, filename="termchat_logs.jsonl"):
        self.filename = filename

    def log_interaction(self, user_input, ai_response):
        """
        Saves a conversation turn to a file for later training.
        """
        entry = {
            "input": user_input,
            "output": ai_response
        }
        
        # Open file in append mode ('a')
        with open(self.filename, 'a') as f:
            f.write(json.dumps(entry) + "\n")
        
        print(f"[DataCollector] Saved interaction to {self.filename}")

    def load_training_data(self):
        """
        Reads the logs to prepare for training.
        """
        if not os.path.exists(self.filename):
            return []
        
        data = []
        with open(self.filename, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data

# Example Usage within TermChat LT
if __name__ == "__main__":
    logger = ChatLogger()
    
    # Simulating a conversation
    user_says = "How do I reset my password?"
    ai_replies = "Go to settings and click reset."
    
    # 1. Log it
    logger.log_interaction(user_says, ai_replies)
    
    # 2. Later, load it to train the model
    training_data = logger.load_training_data()
    print(f"Ready to train on {len(training_data)} examples.")