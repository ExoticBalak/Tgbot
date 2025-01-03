const TelegramBot = require('node-telegram-bot-api');

// Your bot's token
const token = '7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI';

// Create a new bot instance
const bot = new TelegramBot(token, { polling: true });

// Handle /start command
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  const greeting = "Hello! Welcome to the bot. Send me your name, and I'll create a beautiful card for you!";
  bot.sendMessage(chatId, greeting);
});

// Handle text messages
bot.on('message', (msg) => {
  const chatId = msg.chat.id;

  // Ignore the /start command
  if (msg.text !== "/start") {
    const name = msg.text;
    bot.sendMessage(chatId, `Got it, ${name}! Let me generate your card...`);

    // Generate and send a simple text-based card
    bot.sendMessage(chatId, `Here is your card: 🎉 ${name}`);
  }
});
