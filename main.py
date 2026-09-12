import os
import asyncio

import telebot
from dotenv import load_dotenv
import edge_tts

from keyboards import (
    language_keyboard,
    voice_keyboard,
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

user_messages = {}

bot = telebot.TeleBot(BOT_TOKEN)


def get_settings_text(language, voice):
    languages = {
        "en": "🇺🇸 English",
        "fa": "🇮🇷 فارسی",
        "fr": "🇫🇷 Français",
        "de": "🇩🇪 Deutsch"
    }

    voices = {
        "male": "👨 Male",
        "female": "👩 Female"
    }

    return (
        "🎙️ Text2Voice\n\n"
        f"🌍 Language: {languages[language]}\n"
        f"🎙️ Voice: {voices[voice]}\n\n"
        "Send me your text 👇"
    )


def delete_previous_messages(user_id, chat_id):

    if user_id not in user_messages:
        return

    messages = user_messages[user_id]

    for key in [
        "user_message",
        "status_message",
        "audio_message"
    ]:

        message_id = messages.get(key)

        if message_id:

            try:
                bot.delete_message(
                    chat_id,
                    message_id
                )
            except Exception:
                pass

    # Keep settings message
    settings_message = messages.get(
        "settings_message"
    )

    user_messages[user_id] = {
        "settings_message": settings_message
    }


@bot.message_handler(commands=["start"])
def start(message):

    user_id = message.from_user.id
    language, voice = get_user_settings(user_id)

    if user_id in user_messages:
        delete_previous_messages(
            user_id,
            message.chat.id
        )

    settings_message = bot.send_message(
        message.chat.id,
        get_settings_text(language, voice),
        reply_markup=settings_keyboard()
    )

    user_messages[user_id] = {
        "settings_message": settings_message.message_id
    }


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

    language, voice = get_user_settings(
        call.from_user.id
    )

    bot.edit_message_text(
        get_settings_text(
            language,
            voice
        ),
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

    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    # Delete previous messages
    delete_previous_messages(
        user_id,
        chat_id
    )

    # Save current user message
    user_messages[user_id] = {
        "user_message": message.message_id
    }

    language, selected_voice = get_user_settings(
        user_id
    )

    voice = VOICES[language][selected_voice]

    filename = f"voice_{user_id}.mp3"

    # Send status message
    status_message = bot.send_message(
        chat_id,
        "⏳ Preparing your audio..."
    )

    user_messages[user_id]["status_message"] = (
        status_message.message_id
    )

    try:

        asyncio.run(
            generate_audio(
                text,
                voice,
                filename
            )
        )

        # Delete status message
        bot.delete_message(
            chat_id,
            status_message.message_id
        )

        # Send audio
        with open(filename, "rb") as audio:

            audio_message = bot.send_audio(
                chat_id,
                audio
            )

        # Save audio message ID
        user_messages[user_id]["audio_message"] = (
            audio_message.message_id
        )

    except Exception as error:

        print(f"TTS Error: {error}")

        try:
            bot.delete_message(
                chat_id,
                status_message.message_id
            )
        except Exception:
            pass

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
