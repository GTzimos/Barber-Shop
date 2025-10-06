import sqlite3

def connect_db():
    conn = sqlite3.connect("ratings.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5)
        )
    """)
    conn.commit()
    conn.close()

def add_rating(username, rating):
    conn = sqlite3.connect("ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (username, rating) VALUES (?, ?)", (username, rating))
    conn.commit()
    conn.close()

def get_average_rating():
    conn = sqlite3.connect("ratings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating) FROM ratings")
    avg = cursor.fetchone()[0]
    conn.close()
    return round(avg, 2) if avg else None