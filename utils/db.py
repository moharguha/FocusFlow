import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT, password TEXT, premium INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
        username TEXT, task TEXT, deadline TEXT, priority TEXT, done INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS sessions (
        username TEXT, date TEXT, minutes INTEGER
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS streaks (
    username TEXT, last_date TEXT, streak INTEGER
)""")

    conn.commit()
import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        title TEXT,
        priority TEXT,
        scheduled_date TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()