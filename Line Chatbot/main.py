from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import requests
import threading
from pydantic_ai import Agent, RunContext, settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize the AI agent
agent = Agent(model="google-gla:gemini-1.5-flash",
              system_prompt=""" You are helpful assistant name Poppy working for Naz Craftman company.
                               This company is about construction company""",
              model_settings={'temperature': 0.2})

# Message history dictionary to store conversations by user ID
user_conversations = {}

# Line Messaging API constants
LINE_MESSAGING_API = "https://api.line.me/v2/bot/message/reply"
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# Helper function to send a reply to Line
def send_line_reply(reply_token, message_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    
    try:
        response = requests.post(LINE_MESSAGING_API, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Error sending message to Line: {response.text}")
        return response
    except Exception as e:
        print(f"Failed to send message to Line: {e}")
        return None

# Process message in a separate thread
def process_and_reply(message_text, reply_token, user_id):
    try:
        # Get or initialize user conversation history
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        # Run AI with the user's message and their conversation history
        result = agent.run_sync(message_text, message_history=user_conversations[user_id])
        
        # Update conversation history
        user_conversations[user_id] = result.new_messages()
        
        # Get AI response
        ai_response = result.data
        
        # Reply to user
        send_line_reply(reply_token, ai_response)
        
        print(f"Successfully processed and replied to message from user: {user_id}")
    except Exception as e:
        print(f"Error in processing thread: {e}")

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Parse JSON payload from the incoming request
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e
    
    try:
        events = payload.get("events", [])
        if events:
            event = events[0]
            
            # Only process message events
            if event["type"] == "message" and event["message"]["type"] == "text":
                message_text = event["message"]["text"]
                reply_token = event["replyToken"]
                user_id = event["source"]["userId"]
                
                print(f"Received message: '{message_text}' from user: {user_id}")
                
                # Start a new thread to process the message and reply
                thread = threading.Thread(
                    target=process_and_reply,
                    args=(message_text, reply_token, user_id)
                )
                thread.daemon = True
                thread.start()
                
                print(f"Started processing thread for user: {user_id}")
        
    except KeyError as e:
        print(f"Failed to process webhook: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Return a success response immediately to acknowledge receipt of the webhook
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)