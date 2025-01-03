import random
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# Get the port from the environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

# Your bot's token
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"

# List of random greeting quotes
greeting_quotes = [
    "Hello! You're amazing! 💫",
    "Welcome! Let's create something beautiful today! 🌟",
    "Hey there! Ready to create your custom card? 🎨",
    "Hi! I'm here to make your card special! ✨"
]

# Function to get a random greeting quote
def get_random_greeting():
    return random.choice(greeting_quotes)

# Main Menu Options
menu_options = """
Please choose one of the following options:
1. /help - Get help
2. /info - Learn about the bot
3. /customize - Start customizing your card
"""

# Dictionary to track user state
user_state = {}

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# Define the webhook endpoint
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print("Received data:", data)

    if "message" in data:
        message = data["message"]
        if "text" in message:
            text = message["text"]
            chat_id = message["chat"]["id"]

            # Handle /start command
            if text == "/start":
                greeting = get_random_greeting()
                send_message(chat_id, greeting)
                send_message(chat_id, menu_options)
                user_state[chat_id] = "waiting_for_menu"

            # Handle menu options
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_menu":
                if text == "/help":
                    send_message(chat_id, "This bot helps you create custom greeting cards with your name!")
                elif text == "/info":
                    send_message(chat_id, "This bot was created to let you design beautiful custom cards with different backgrounds, text styles, and more.")
                elif text == "/customize":
                    send_message(chat_id, "Let's start customizing your card! Choose the background style (color, gradient, or design):")
                    user_state[chat_id] = "waiting_for_background_style"
            
            # Handle background style customization
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_background_style":
                if text in ["color", "gradient", "design"]:
                    user_state[chat_id + "_background_style"] = text
                    send_message(chat_id, f"Background style set to {text}. Now, choose the text size (small, medium, large):")
                    user_state[chat_id] = "waiting_for_text_size"
                else:
                    send_message(chat_id, "Invalid choice! Please choose between 'color', 'gradient', or 'design'.")

            # Handle text size customization
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_text_size":
                if text in ["small", "medium", "large"]:
                    user_state[chat_id + "_text_size"] = text
                    send_message(chat_id, "Text size set. Now, choose the font style (e.g., Arial, Times New Roman):")
                    user_state[chat_id] = "waiting_for_font"
                else:
                    send_message(chat_id, "Invalid size! Please choose 'small', 'medium', or 'large'.")
            
            # Handle font style customization
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_font":
                user_state[chat_id + "_font"] = text
                send_message(chat_id, "Font style set. Now, choose the resolution (small, medium, large):")
                user_state[chat_id] = "waiting_for_resolution"

            # Handle resolution customization
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_resolution":
                if text in ["small", "medium", "large"]:
                    user_state[chat_id + "_resolution"] = text
                    send_message(chat_id, "Resolution set. Please send your name:")
                    user_state[chat_id] = "waiting_for_name"
                else:
                    send_message(chat_id, "Invalid resolution! Please choose 'small', 'medium', or 'large'.")

            # Handle name input and generate the card
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_name":
                user_state[chat_id + "_name"] = text
                send_message(chat_id, f"Name set to {text}. Generating your card...")
                
                # Generate the card image with user preferences
                img = generate_card_image(chat_id)
                
                # Save image to a byte buffer
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)

                # Send the image as a file
                files = {'photo': ('card.png', img_byte_arr, 'image/png')}
                send_image(chat_id, files)
                send_message(chat_id, f"Your custom card has been created with the name {text}!")

    return "OK"

# Function to send a message back to the user
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Function to send an image to the user
def send_image(chat_id, files):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {'chat_id': chat_id}
    requests.post(url, data=payload, files=files)

# Function to generate a greeting card image based on user preferences
def generate_card_image(chat_id):
    # Set defaults or get from user state
    background_style = user_state.get(chat_id + "_background_style", "color")
    text_size = user_state.get(chat_id + "_text_size", "medium")
    font_style = user_state.get(chat_id + "_font", "Arial")
    resolution = user_state.get(chat_id + "_resolution", "medium")
    name = user_state.get(chat_id + "_name", "User")

    # Set dimensions based on resolution choice
    if resolution == "small":
        width, height = 300, 200
    elif resolution == "medium":
        width, height = 500, 300
    else:
        width, height = 700, 400

    # Create a blank image
    img = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Draw on the image
    draw = ImageDraw.Draw(img)
    
    # Set text size based on user choice
    if text_size == "small":
        font_size = 20
    elif text_size == "medium":
        font_size = 40
    else:
        font_size = 60

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Draw the user's name on the image
    text_width, text_height = draw.textsize(name, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, name, font=font, fill="black")

    return img

if __name__ == "__main__":
    # Run Flask on the port provided by Render (or default to 5000)
    app.run(host="0.0.0.0", port=port)
