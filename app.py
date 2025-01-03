from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Get the port from the environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

# Your bot's token
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"

# Define a simple home route for debugging
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

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
    # Run Flask on the port provided by Render (or default to 5000)
    app.run(host="0.0.0.0", port=port)
