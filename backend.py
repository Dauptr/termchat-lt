import openai
import os
from termAi.models import SimpleChatBot
from termAi.data_collector import ChatLogger

# Initialize local AI and logger
local_bot = SimpleChatBot()
logger = ChatLogger()

def get_ai_response(user_message, use_api=False):
    try:
        if use_api and os.getenv("OPENAI_API_KEY"):
            client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are TermAi, a helpful assistant in TermChat LT. Respond in Lithuanian when possible."},
                    {"role": "user", "content": user_message}
                ]
            )
            ai_response = response.choices[0].message.content
        else:
            # Use local termAi library
            ai_response = local_bot.think(user_message)
        
        # Log interaction for training
        logger.log_interaction(user_message, ai_response)
        return ai_response
        
    except Exception as e:
        # Fallback to local AI on any error
        ai_response = local_bot.think(user_message)
        logger.log_interaction(user_message, ai_response)
        return ai_response