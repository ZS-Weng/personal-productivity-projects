import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pomodoro.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pomo_logs (
            date TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    return conn

def get_pomos(date: str) -> int:
    conn = get_db()
    row = conn.execute("SELECT count FROM pomo_logs WHERE date = ?", (date,)).fetchone()
    conn.close()
    return row[0] if row else 0

def set_pomos(date: str, count: int) -> int:
    conn = get_db()
    conn.execute(
        "INSERT INTO pomo_logs (date, count) VALUES (?, ?) ON CONFLICT(date) DO UPDATE SET count = ?",
        (date, count, count)
    )
    conn.commit()
    conn.close()
    return count

def increment_pomos(date: str) -> int:
    conn = get_db()
    conn.execute(
        "INSERT INTO pomo_logs (date, count) VALUES (?, 1) ON CONFLICT(date) DO UPDATE SET count = count + 1",
        (date,)
    )
    conn.commit()
    row = conn.execute("SELECT count FROM pomo_logs WHERE date = ?", (date,)).fetchone()
    conn.close()
    return row[0]

def get_all_pomos() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT date, count FROM pomo_logs ORDER BY date").fetchall()
    conn.close()
    return [{"date": r[0], "count": r[1]} for r in rows]