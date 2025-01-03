from flask import Flask, request
import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# Store user state to track the progress of customization
user_state = {}

# Some dummy random greetings
greetings = [
    "Hello, welcome to your custom card bot!",
    "Hi there! Let's create something amazing together.",
    "Welcome! Ready to create your custom card?"
]

# Bot's token and URL
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"
RENDER_URL = "https://tgbot-6qe5.onrender.com"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"
    
# Route for the webhook
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

                # Handle background style customization
                elif chat_id in user_state and user_state[chat_id] == "waiting_for_background_style":
                    if text in ["color", "gradient", "design"]:
                        user_state[chat_id + "_background_style"] = text
                        send_message(chat_id, f"Background style set to {text}. Now, choose the text size (small, medium, large):")
                        user_state[chat_id] = "waiting_for_text_size"
                    else:
                        send_message(chat_id, "Invalid choice! Please choose 'color', 'gradient', or 'design'.")

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
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error processing webhook", 500


# Function to send a message
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Function to send an image
def send_image(chat_id, files):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id}
    requests.post(url, files=files, data=payload)

# Function to generate a custom card image
def generate_card_image(chat_id):
    # Get user preferences from state
    background_style = user_state.get(chat_id + "_background_style", "color")
    text_size = user_state.get(chat_id + "_text_size", "medium")
    font = user_state.get(chat_id + "_font", "Arial")
    resolution = user_state.get(chat_id + "_resolution", "medium")
    name = user_state.get(chat_id + "_name", "User")

    # Create a basic image with a white background
    img = Image.new('RGB', (500, 300), color='white')

    # Get a font
    try:
        font = ImageFont.truetype(f"{font}.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)
    text = f"Hello, {name}"

    # Draw the text on the image
    draw.text((100, 100), text, font=font, fill='black')

    return img


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
