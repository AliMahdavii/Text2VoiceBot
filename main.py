import os

import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! I'm Text2Voice Bot 🎙️")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)


print("Bot is running...")

bot.infinity_polling()
