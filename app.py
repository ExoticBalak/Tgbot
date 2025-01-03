from flask import Flask, request
import requests

app = Flask(__name__)

# Your bot's token
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"

# Define the webhook endpoint
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print("Received data:", data)  # Debugging log
    
    # Example: Process the "/start" command
    if "message" in data:
        message = data["message"]
        if "text" in message:
            text = message["text"]
            chat_id = message["chat"]["id"]
            if text == "/start":
                send_message(chat_id, "Welcome! Send me your name and I'll create a card for you.")
    
    return "OK"

# Function to send a message back to the user
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
