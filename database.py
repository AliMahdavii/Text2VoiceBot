import sqlite3


DATABASE_NAME = "bot.db"


def connect():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_language(user_id, language):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, language)
        VALUES (?, ?)
    """, (user_id, language))

    connection.commit()
    connection.close()


def get_language(user_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT language FROM users WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return "en"
