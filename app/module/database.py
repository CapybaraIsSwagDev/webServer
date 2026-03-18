import sqlite3
from pathlib import Path

# -----------------------------
# Database setup
# -----------------------------
db_path = Path(__file__).parent.parent.joinpath("users.db")

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as db:
    # Create table if it doesn't exist
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT,
        xp INTEGER DEFAULT 0,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS user_lesson_completions (
        user_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        -- This prevents duplicate entries for the same user/lesson combo
        PRIMARY KEY (user_id, lesson_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    );
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        template TEXT NOT NULL,         -- 'code', 'quiz', 'video'
        title TEXT NOT NULL,
        difficulty INTEGER,
        xp TEXT,
        -- All varying fields go here as a JSON object
        data JSON NOT NULL 
    );
    """)
    # Check if 'xp' column exists (migration for old DBs)
    cursor = db.execute("PRAGMA table_info(users)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "xp" not in columns:
        db.execute("ALTER TABLE users ADD COLUMN xp INTEGER DEFAULT 0")