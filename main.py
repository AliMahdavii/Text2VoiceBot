import os

import telebot
from dotenv import load_dotenv
from gtts import gTTS


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Hello! Send me any text and I'll turn it into audio 🎙️"
    )


@bot.message_handler(func=lambda message: True)
def text_to_speech(message):

    text = message.text

    tts = gTTS(
        text=text,
        lang="en"
    )

    filename = "voice.mp3"

    tts.save(filename)

    with open(filename, "rb") as audio:
        bot.send_audio(
            message.chat.id,
            audio
        )


print("Bot is running...")

bot.infinity_polling()
