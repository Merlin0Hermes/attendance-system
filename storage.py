from pathlib import Path
import uuid
from PIL import Image
import sqlite3
from datetime import datetime
import streamlit as st

# Database name
DB_PATH = "attendance.db"
IMG_DIR = "database/"

# Connect to database
def connect():
    return sqlite3.connect(DB_PATH)

def get_user_id_by_name(name) -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE name = ?", (name,)
        ).fetchall()
        return row[0][0]


def add_user(username: str,):
    with connect() as conn:
        conn.execute("INSERT INTO users (name) VALUES (?)", (username,))



# Create table
def create_tables():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filepath TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)


    Path(IMG_DIR).mkdir(parents=True, exist_ok=True)


def get_name_by_filepath(filepath):
    user_id = st.session_state.user_id
    with connect() as conn:
        row = conn.execute(
            "SELECT name FROM images WHERE filepath = ? AND user_id = ?", (filepath, user_id)
        ).fetchall()
        return row[0][0]


def db_empty():
    with connect() as conn:
        data = conn.execute("SELECT * FROM images").fetchall()
        return len(data) == 0


def exists_name(name):
    user_id = st.session_state.user_id
    with connect() as conn:
        data = conn.execute(
            "SELECT * FROM images WHERE name LIKE ? AND user_id = ?", (name, user_id)
        ).fetchall()
        return len(data) != 0


def save_image(name: str, image: Image.Image):
    user_id = st.session_state.user_id
    filename = uuid.uuid4().hex
    filepath = f"{IMG_DIR}/{filename}.png"
    image.save(filepath, "PNG")
    with connect() as conn:
        conn.execute(
            "INSERT INTO images (name, filepath, user_id) VALUES (?, ?, ?)",
            (name.title(), filepath, user_id),
        )


def load_name_imgpath():
    user_id = st.session_state.user_id
    with connect() as conn:
        data = conn.execute(
            "SELECT id, name, filepath FROM images WHERE user_id = ? ORDER BY name", (user_id,)
        ).fetchall()
        return [{"id": row[0], "name": row[1], "filepath": row[2]} for row in data]


def remove_image(row):
    user_id = st.session_state.user_id
    with connect() as conn:
        conn.execute("DELETE FROM images WHERE id = ? AND user_id = ?", (row["id"], user_id))
    Path.unlink(row["filepath"])


# Mark attendance
def mark_attendance(name):
    user_id = st.session_state.user_id
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO attendance (name, date, time, user_id) VALUES (?, ?, ?, ?)",
                (name, date, time, user_id),
            )
    except sqlite3.IntegrityError:
        return f"{name} already marked today"


# Get attendance
def get_attendance():
    user_id = st.session_state.user_id
    with connect() as conn:
        data = conn.execute(
            "SELECT name, date, time FROM attendance WHERE user_id = ? ORDER BY date DESC, time DESC", (user_id,)
        ).fetchall()

    return [{"name": row[0], "date": row[1], "time": row[2]} for row in data]


def clear_attendance():
    user_id = st.session_state.user_id
    with connect() as conn:
        conn.execute("DELETE FROM attendance WHERE user_id = ?", (user_id,))
