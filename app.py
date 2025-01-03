from flask import Flask, request
import requests
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Webhook route
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text.startswith("/start"):
            send_message(chat_id, "Welcome! Send me your name, and I'll create a card for you.")
        else:
            # Generate the card
            card_image = create_card(text)
            
            # Send the card to the user
            send_photo(chat_id, card_image)

    return "ok"

def create_card(name):
    # Create a blank image
    width, height = 800, 400
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Add background patterns/colors
    for i in range(0, width, 50):
        draw.line((i, 0, i, height), fill=(200, 230, 255), width=5)

    # Add text
    font = ImageFont.truetype("arial.ttf", 60)  # Make sure this font is available
    text_width, text_height = draw.textsize(name, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), name, fill="blue", font=font)

    # Save to bytes
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_photo(chat_id, photo):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": photo}
    payload = {"chat_id": chat_id}
    requests.post(url, data=payload, files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
