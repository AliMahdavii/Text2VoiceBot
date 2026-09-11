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
            language TEXT NOT NULL,
            voice TEXT NOT NULL DEFAULT 'male'
        )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "voice" not in columns:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN voice TEXT NOT NULL DEFAULT 'male'
        """)

    connection.commit()
    connection.close()


def save_language(user_id, language):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT voice FROM users WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE users
            SET language = ?
            WHERE user_id = ?
        """, (language, user_id))

    else:
        cursor.execute("""
            INSERT INTO users (user_id, language, voice)
            VALUES (?, ?, ?)
        """, (user_id, language, "male"))

    connection.commit()
    connection.close()


def save_voice(user_id, voice):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET voice = ?
        WHERE user_id = ?
    """, (voice, user_id))

    connection.commit()
    connection.close()


def get_user_settings(user_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT language, voice
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0], result[1]

    return "en", "male"
