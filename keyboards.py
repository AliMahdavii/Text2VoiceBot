from telebot import types


def language_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    english = types.InlineKeyboardButton(
        "🇺🇸 English",
        callback_data="lang_en"
    )

    persian = types.InlineKeyboardButton(
        "🇮🇷 فارسی",
        callback_data="lang_fa"
    )

    french = types.InlineKeyboardButton(
        "🇫🇷 Français",
        callback_data="lang_fr"
    )

    german = types.InlineKeyboardButton(
        "🇩🇪 Deutsch",
        callback_data="lang_de"
    )

    keyboard.add(english, persian)
    keyboard.add(french, german)

    return keyboard
