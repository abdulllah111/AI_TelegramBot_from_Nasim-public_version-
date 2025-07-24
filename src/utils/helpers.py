import json
import logging
import os
from telegram import User

DATA_DIR = "src/data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def load_json(file_path: str) -> dict | list:
    """Loads data from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Error loading JSON from {file_path}: {e}")
        return {}

def save_json(file_path: str, data: dict | list) -> None:
    """Saves data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Error saving JSON to {file_path}: {e}")

def get_or_create_user(user: User) -> None:
    """Checks if a user exists in the database, and if not, adds them."""
    users = load_json(USERS_FILE)
    user_id = str(user.id)

    if user_id not in users:
        users[user_id] = {
            "username": user.username,
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_bot": user.is_bot,
            "language_code": user.language_code,
        }
        save_json(USERS_FILE, users)
        logging.info(f"New user created: {user.full_name} ({user_id})")

def load_chat_history(user_id: int) -> list[dict]:
    """Loads the chat history for a specific user."""
    history_file = os.path.join(DATA_DIR, f"chats_{user_id}.json")
    history = load_json(history_file)
    # Ensure it returns a list
    return history if isinstance(history, list) else []

def save_chat_history(user_id: int, history: list[dict]) -> None:
    """Saves the chat history for a specific user."""
    history_file = os.path.join(DATA_DIR, f"chats_{user_id}.json")
    save_json(history_file, history)
