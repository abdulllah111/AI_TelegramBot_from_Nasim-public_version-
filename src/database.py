import sqlite3
import logging
from datetime import datetime

def initialize_database():
    """Initializes the database and creates tables if they don't exist."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            # Create requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    request_text TEXT NOT NULL,
                    response_text TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        raise

def add_user(user_id: int, username: str, first_name: str, last_name: str):
    """Adds a new user to the database or updates existing user's name."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if cursor.fetchone() is None:
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    "INSERT INTO users (id, username, first_name, last_name, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username, first_name, last_name, created_at)
                )
                logging.info(f"New user {first_name} ({user_id}) added to the database.")
            else:
                cursor.execute(
                    "UPDATE users SET username = ?, first_name = ?, last_name = ? WHERE id = ?",
                    (username, first_name, last_name, user_id)
                )
                logging.info(f"User {first_name} ({user_id}) data updated.")
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to add or update user {user_id}: {e}")

def add_request(user_id: int, request_text: str, response_text: str):
    """Adds a new request to the database."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO requests (user_id, request_text, response_text, created_at) VALUES (?, ?, ?, ?)",
                (user_id, request_text, response_text, created_at)
            )
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to log request for user {user_id}: {e}")

def get_user_count() -> int:
    """Returns the total number of users."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        logging.error(f"Failed to get user count: {e}")
        return 0

def get_user_history(user_id: int, limit: int = 10):
    """Retrieves the chat history for a specific user."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT request_text, response_text FROM requests WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)
            )
            history = []
            for row in cursor.fetchall():
                history.append({"role": "user", "content": row[0]})
                if row[1]:
                    history.append({"role": "assistant", "content": row[1]})
            return history
    except sqlite3.Error as e:
        logging.error(f"Failed to retrieve history for user {user_id}: {e}")
        return []

def get_all_users():
    """Returns all users from the database."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, first_name, username FROM users ORDER BY created_at DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Failed to get all users: {e}")
        return []

def clear_user_history(user_id: int):
    """Clears the request history for a specific user."""
    try:
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM requests WHERE user_id = ?", (user_id,))
            conn.commit()
            logging.info(f"History for user {user_id} cleared.")
    except sqlite3.Error as e:
        logging.error(f"Failed to clear history for user {user_id}: {e}")
