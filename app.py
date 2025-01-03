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
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error processing webhook", 500
