import os
import asyncio

import telebot
from dotenv import load_dotenv
import edge_tts

from keyboards import (
    language_keyboard,
    voice_keyboard,
    change_language_keyboard,
    settings_keyboard
)

from database import (
    create_table,
    save_language,
    save_voice,
    get_user_settings
)

from voices import VOICES


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
        "🎙️ Choose your voice:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=voice_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("voice_")
)
def select_voice(call):
    voice = call.data.replace("voice_", "")

    save_voice(
        call.from_user.id,
        voice
    )

    bot.answer_callback_query(
        call.id,
        "Voice selected ✅"
    )

    bot.edit_message_text(
        "✅ Settings saved!\n\n"
        "Now send me some text 🎙️",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=settings_keyboard()
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


@bot.callback_query_handler(
    func=lambda call: call.data == "change_voice"
)
def change_voice(call):
    bot.answer_callback_query(call.id)

    bot.edit_message_text(
        "🎙️ Choose your new voice:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=voice_keyboard()
    )


async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(filename)


@bot.message_handler(func=lambda message: True)
def text_to_speech(message):
    text = message.text

    language, selected_voice = get_user_settings(
        message.from_user.id
    )

    voice = VOICES[language][selected_voice]

    filename = f"voice_{message.from_user.id}.mp3"

    try:
        asyncio.run(
            generate_audio(
                text,
                voice,
                filename
            )
        )

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
