import os

import telebot
from dotenv import load_dotenv
from gtts import gTTS
import asyncio
import edge_tts

from keyboards import (
    language_keyboard,
    change_language_keyboard
)

from database import (
    create_table,
    save_language,
    get_language
)


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎙️ Welcome to Text2Voice Bot!\n\n"
        "Choose your language:",
        reply_markup=language_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("lang_")
)
def select_language(call):
    language = call.data.replace("lang_", "")

    save_language(
        call.from_user.id,
        language
    )

    bot.answer_callback_query(
        call.id,
        "Language selected ✅"
    )

    bot.edit_message_text(
        "✅ Language selected!\n\n"
        "Now send me some text 🎙️",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=change_language_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "change_language"
)
def change_language(call):
    bot.answer_callback_query(call.id)

    bot.edit_message_text(
        "🌍 Choose your new language:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=language_keyboard()
    )


async def generate_persian_audio(text, filename):
    communicate = edge_tts.Communicate(
        text,
        "fa-IR-FaridNeural"
    )

    await communicate.save(filename)


@bot.message_handler(func=lambda message: True)
def text_to_speech(message):
    text = message.text

    language = get_language(
        message.from_user.id
    )

    filename = f"voice_{message.from_user.id}.mp3"

    try:

        if language == "fa":
            asyncio.run(
                generate_persian_audio(
                    text,
                    filename
                )
            )

        else:
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

    except Exception as error:
        print(f"TTS Error: {error}")

        bot.reply_to(
            message,
            "❌ Sorry, I couldn't generate the audio."
        )

    finally:
        if os.path.exists(filename):
            os.remove(filename)


create_table()

print("Bot is running...")

bot.infinity_polling()
