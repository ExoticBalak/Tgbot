from flask import Flask, request
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# Get the port from the environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

# Your bot's token
BOT_TOKEN = "7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI"

# Store the state of the user (whether they're waiting for a name)
user_state = {}

# Define a simple home route for debugging
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# Define the webhook endpoint
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print("Received data:", data)  # Debugging log

    # Check if there's a message
    if "message" in data:
        message = data["message"]
        if "text" in message:
            text = message["text"]
            chat_id = message["chat"]["id"]

            # If it's the /start command, ask for the name
            if text == "/start":
                send_message(chat_id, "Welcome! Send me your name and I'll create a card for you.")
                user_state[chat_id] = "waiting_for_name"

            # If user is in 'waiting_for_name' state, generate the card with the name
            elif chat_id in user_state and user_state[chat_id] == "waiting_for_name":
                user_state[chat_id] = "name_received"
                name = message["text"]
                send_card(chat_id, name)

    return "OK"

# Function to send a message back to the user
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Function to generate a card image and send it
def send_card(chat_id, name):
    # Create an image with the name
    image = create_card_image(name)
    
    # Convert the image to a byte array to send it via Telegram API
    image_byte_array = image_to_byte_array(image)
    
    # Send the image to the user
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': ('card.png', image_byte_array, 'image/png')}
    payload = {'chat_id': chat_id}
    requests.post(url, data=payload, files=files)

# Function to create a card image with the user's name
def create_card_image(name):
    # Create a blank white image
    image = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()
    
    # Add the name text to the image
    text = f"Hello, {name}!"
    text_width, text_height = draw.textsize(text, font)
    position = ((400 - text_width) // 2, (200 - text_height) // 2)  # Center the text
    draw.text(position, text, fill="black", font=font)

    return image

# Function to convert image to byte array
def image_to_byte_array(image):
    byte_array = io.BytesIO()
    image.save(byte_array, format='PNG')
    byte_array.seek(0)
    return byte_array

if __name__ == "__main__":
    # Run Flask on the port provided by Render (or default to 5000)
    app.run(host="0.0.0.0", port=port)
