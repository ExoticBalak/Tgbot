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

                # Handle background customization
                elif chat_id in user_state and user_state[chat_id] == "waiting_for_background_style":
                    # Save background style (for now just a placeholder)
                    send_message(chat_id, "Background style selected. Now, choose your text style: font, size, etc.")
                    user_state[chat_id] = "waiting_for_text_style"

                # Handle text style customization
                elif chat_id in user_state and user_state[chat_id] == "waiting_for_text_style":
                    send_message(chat_id, "Text style selected. Now, please provide your name to create the card.")
                    user_state[chat_id] = "waiting_for_name"

                # Handle final step after receiving the name
                elif chat_id in user_state and user_state[chat_id] == "waiting_for_name":
                    name = text  # Save the name entered by the user
                    print(f"User's name: {name}")

                    # Generate the card image with the name and the customization options chosen
                    generate_card_image(name)  # Function to generate the card image (you'll need to implement this)
                    
                    send_message(chat_id, "Here is your custom card!")
                    # Reset the user state after processing
                    user_state[chat_id] = None
                    print("User state reset")

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

# Function to generate card image with user’s name
def generate_card_image(name):
    # Create a blank image with some basic dimensions
    width, height = 400, 200
    img = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Initialize drawing context
    draw = ImageDraw.Draw(img)

    # Set font and size
    font = ImageFont.load_default()
    
    # Add user's name to the card
    text = f"Hello, {name}!"
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill="black", font=font)

    # Save the image
    img.save(f"/tmp/{name}_card.png")
    print(f"Card saved as /tmp/{name}_card.png")

# Run the app on Render or local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
