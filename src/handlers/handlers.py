import logging
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from src.config import ADMIN_ID
from src.services.gpt import generate_response
from src.utils.helpers import get_or_create_user, load_chat_history, save_chat_history

# Define a constant for the system prompt
SYSTEM_PROMPT = """Ты являешься личным smm специалистом, который помогает пользователям продвигать их аккаунты в социальных сетях."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Привет! Я твой личный SMM-ассистент. Спроси меня о чем-нибудь.")

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the user's chat history."""
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    history_path = f"src/data/chats_{user_id}.json"
    if os.path.exists(history_path):
        try:
            # Rename the file to archive it
            archive_path = f"src/data/chats_{user_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            os.rename(history_path, archive_path)
            message = "История переписки очищена и заархивирована."
        except Exception as e:
            logging.error(f"Error clearing history for user {user_id}: {e}")
            message = "Произошла ошибка при очистке истории."
    else:
        message = "История переписки уже пуста."

    await update.message.reply_text(message)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user = update.message.from_user
    user_id = user.id
    message_text = update.message.text

    logging.info(f"Message '{message_text}' from {user.full_name} ({user_id})")

    # 1. Check if the user is an admin
    if user_id != ADMIN_ID:
        await update.message.reply_text("Извините, я отвечаю только администратору.")
        # Optionally, send a voice message like in the old code
        # await update.message.reply_voice(voice=open('path/to/not_admin.mp3', 'rb'))
        return

    # 2. Get or create user profile
    get_or_create_user(user)

    # 3. Load chat history
    history = load_chat_history(user_id)
    if not history:
        history.extend([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Хорошо, я готов помочь с SMM."},
        ])

    # 4. Add user message to history
    history.append({"role": "user", "content": message_text})

    # 5. Generate response
    response_text = await generate_response(history)
    if response_text is None:
        await update.message.reply_text("Произошла ошибка при генерации ответа. Попробуйте позже.")
        return

    # 6. Add assistant response to history and save
    history.append({"role": "assistant", "content": response_text})
    save_chat_history(user_id, history)

    # 7. Send the response to the user
    await update.message.reply_text(response_text)