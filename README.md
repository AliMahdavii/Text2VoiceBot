# 🎙️ Text2VoiceBot

A Telegram bot that converts text into natural-sounding speech and sends it back as an audio file.

Text2VoiceBot supports multiple languages, male and female voices, and stores each user's voice preferences using SQLite.

## ✨ Features

- 🌍 Multilingual text-to-speech
- 🎙️ Male and female voices
- 🇺🇸 English
- 🇮🇷 Persian
- 🇫🇷 French
- 🇩🇪 German
- 💾 Persistent user settings with SQLite
- 🎛️ Interactive Telegram interface
- 🧹 Automatic cleanup of generated audio files
- ⚡ Powered by Microsoft Edge TTS

## 🛠️ Tech Stack

- Python
- pyTelegramBotAPI
- Edge TTS
- SQLite
- python-dotenv

## 📂 Project Structure

```text
Text2VoiceBot/
│
├── main.py
├── database.py
├── keyboards.py
├── voices.py
├── requirements.txt
├── .env
├── .gitignore
└── bot.db
```

🎯 How It Works
Start the bot with /start
Choose your language
Choose a male or female voice
Send any text
The bot converts it to speech
Receive the generated audio directly in Telegram
🔐 Security

Never commit your .env file or Telegram bot token to GitHub.

The bot token should always be stored in environment variables.

