import sqlite3

def init_db():
    conn = sqlite3.connect("eco_bot.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_challenges (
            user_id TEXT,
            year INTEGER,
            week INTEGER,
            challenge_index INTEGER,
            PRIMARY KEY(user_id, year, week)
        )
    ''')
    conn.commit()
    conn.close()