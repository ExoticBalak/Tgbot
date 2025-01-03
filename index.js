const TelegramBot = require('node-telegram-bot-api');

// Your bot's token
const token = '7514750197:AAF4cUNMkMx8ekhIQmG7kZxRZqnRKyueiPI';

// Create a new bot instance
const bot = new TelegramBot(token, { polling: true });

// Store user states
const userStates = {};

// Random greetings
const greetings = [
  "Hello! Ready to create your card?",
  "Hi there! Let's make something amazing!",
  "Hey! Time to customize your card!",
  "Welcome! Let's design your card together!"
];

// Handle /start command
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;

  // Send random greeting and display menu
  const greeting = greetings[Math.floor(Math.random() * greetings.length)];
  bot.sendMessage(chatId, greeting);
  bot.sendMessage(
    chatId,
    "Choose an option:\n1️⃣ /help - Learn how to use the bot\n2️⃣ /customize - Customize your card\n3️⃣ /info - Get info about the bot"
  );
  userStates[chatId] = "menu"; // Set user state to menu
});

// Handle menu options
bot.onText(/\/help/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "This bot lets you create a custom card with your name. Use /customize to get started!");
});

bot.onText(/\/info/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "I am a bot created to generate personalized name cards for you!");
});

bot.onText(/\/customize/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "Great! Let's customize your card. Choose a background style:\n1️⃣ /color\n2️⃣ /gradient\n3️⃣ /design");
  userStates[chatId] = "customizing"; // Set user state to customizing
});

// Handle customization options
bot.onText(/\/color/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "You've selected a solid color background. What color do you want? Reply with a color name (e.g., red, blue).");
  userStates[chatId] = "color";
});

bot.onText(/\/gradient/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "You've selected a gradient background. Please wait while I prepare a random gradient for your card.");
  // Simulate gradient generation
  setTimeout(() => {
    bot.sendMessage(chatId, "Gradient ready! Now, send me your name to create the card.");
    userStates[chatId] = "waiting_for_name";
  }, 2000);
});

bot.onText(/\/design/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, "You've selected a random design background. Now, send me your name to create the card.");
  userStates[chatId] = "waiting_for_name";
});

// Handle name input
bot.on('message', (msg) => {
  const chatId = msg.chat.id;

  if (userStates[chatId] === "color") {
    const color = msg.text.toLowerCase();
    bot.sendMessage(chatId, `You've chosen the color ${color}. Now, send me your name to complete the card.`);
    userStates[chatId] = { stage: "waiting_for_name", background: { type: "color", value: color } };
  } else if (userStates[chatId]?.stage === "waiting_for_name") {
    const name = msg.text;
    bot.sendMessage(chatId, `Got it, ${name}! Let me generate your card...`);

    // Generate a basic card (placeholder)
    bot.sendMessage(chatId, `Here is your card: 🎉 ${name}`);
    userStates[chatId] = null; // Reset user state
  }
});
