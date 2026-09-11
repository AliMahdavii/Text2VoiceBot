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

    # Create a unique filename for each user
    filename = f"voice_{message.from_user.id}.mp3"

    try:
        # Convert text to speech
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        # Send audio to user
        with open(filename, "rb") as audio:
            bot.send_audio(
                message.chat.id,
                audio
            )

    finally:
        # Delete the audio file after sending
        if os.path.exists(filename):
            os.remove(filename)


print("Bot is running...")

bot.infinity_polling()
