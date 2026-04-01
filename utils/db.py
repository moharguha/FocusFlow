import sqlite3

# ✅ ONE DATABASE ONLY
conn = sqlite3.connect("app.db", check_same_thread=False)
c = conn.cursor()

def init_db():

    # =========================
    # 👤 USERS TABLE
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        premium INTEGER DEFAULT 0
    )
    """)

    # =========================
    # 📋 TASKS TABLE (UPDATED)
    # =========================
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

    # =========================
    # ⏱ SESSIONS TABLE
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        username TEXT,
        date TEXT,
        minutes INTEGER
    )
    """)

    # =========================
    # 🔥 STREAK TABLE
    # =========================
    c.execute("""
    CREATE TABLE IF NOT EXISTS streaks (
        username TEXT PRIMARY KEY,
        last_date TEXT,
        streak INTEGER
    )
    """)

    conn.commit()
