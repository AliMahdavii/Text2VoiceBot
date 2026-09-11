import os

import telebot
from dotenv import load_dotenv
from gtts import gTTS

from keyboards import language_keyboard


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

user_languages = {}


@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "🎙️ Welcome to Text2Voice Bot!\n\n"
        "Choose your language:",
        reply_markup=language_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def select_language(call):

    language = call.data.replace("lang_", "")

    user_languages[call.from_user.id] = language

    bot.answer_callback_query(
        call.id,
        "Language selected ✅"
    )

    bot.edit_message_text(
        "✅ Language selected!\n\n"
        "Now send me some text 🎙️",
        call.message.chat.id,
        call.message.message_id
    )


@bot.message_handler(func=lambda message: True)
def text_to_speech(message):

    text = message.text

    language = user_languages.get(
        message.from_user.id,
        "en"
    )

    filename = f"voice_{message.from_user.id}.mp3"

    try:

        tts = gTTS(
            text=text,
            lang=language
        )

        tts.save(filename)

        with open(filename, "rb") as audio:
            bot.send_audio(
                message.chat.id,
                audio
            )

    finally:

        if os.path.exists(filename):
            os.remove(filename)


print("Bot is running...")

bot.infinity_polling()
