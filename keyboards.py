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


def voice_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    male = types.InlineKeyboardButton(
        "👨 Male",
        callback_data="voice_male"
    )

    female = types.InlineKeyboardButton(
        "👩 Female",
        callback_data="voice_female"
    )

    keyboard.add(male, female)

    return keyboard


def settings_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    change_language = types.InlineKeyboardButton(
        "🌍 Change Language",
        callback_data="change_language"
    )

    change_voice = types.InlineKeyboardButton(
        "🎙️ Change Voice",
        callback_data="change_voice"
    )

    keyboard.add(change_language)
    keyboard.add(change_voice)

    return keyboard
