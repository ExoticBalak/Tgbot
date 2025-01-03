from flask import Flask, request
import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# This route will confirm the bot is running
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# Your bot's token and Render URL
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"
RENDER_URL = "https://tgbot-6qe5.onrender.com"

# Placeholder for user states, this will be useful for handling different user interactions
user_state = {}

# Random greetings
greetings = [
    "Hello! How can I assist you today?",
    "Hey there! Welcome to the bot!",
    "Hi! Ready to make your card?",
    "Greetings! Let's create something amazing together!"
]

# Updated webhook route with error handling
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Received data:", data)  # Debugging log
        
        if "message" in data:
            message = data["message"]
            if "text" in message:
                text = message["text"]
                chat_id = message["chat"]["id"]

                # Handle /start command
                if text == "/start":
                    greeting = random.choice(greetings)
                    send_message(chat_id, greeting)
                    send_message(chat_id, "Choose from the options below:\n/help - Get help\n/info - Get info\n/customize - Start customizing your card.")
                    user_state[chat_id] = "waiting_for_menu"

                # Handle menu options
                elif chat_id in user_state and user_state[chat_id] == "waiting_for_menu":
                    if text == "/help":
                        send_message(chat_id, "This bot lets you create a custom card with your name and a personalized design.")
                    elif text == "/info":
                        send_message(chat_id, "The bot helps you create beautiful greeting cards with custom text, background, and other features.")
                    elif text == "/customize":
                        send_message(chat_id, "Let's start customizing your card!\nChoose a background style (color, gradient, design):")
                        user_state[chat_id] = "waiting_for_background_style"

                # Continue with other steps...

        return "OK"
    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error to understand what's going wrong
        send_message(chat_id, "Oops! Something went wrong. Please try again later.")  # Notify the user
        return "Error processing webhook", 500

# Function to send a message back to the user
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Run the app on Render or local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
