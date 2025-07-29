import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import TimedOut
from telegram.ext import ContextTypes, ConversationHandler
from src.config import ADMIN_ID
from src.services.gpt import generate_response
from src.database import add_user, add_request, get_user_count, get_user_history, get_all_users, clear_user_history

# Define a constant for the system prompt
SYSTEM_PROMPT = """Ты являешься личным smm специалистом, который помогает пользователям продвигать их аккаунты в социальных сетях."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Привет! Я твой личный SMM-ассистент. Спроси меня о чем-нибудь.")

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the user's chat history."""
    user_id = update.message.from_user.id

    if text == "✍️ Написать ассистенту":
        await update.message.reply_text("Напиши свой вопрос:", reply_markup=ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True))
        return TYPING_REPLY
    elif text == "Очистить историю":
        clear_user_history(user_id)
        await update.message.reply_text("История сообщений очищена.")
        return MAIN_MENU
    elif text == "Панель администратора" and user_id == ADMIN_ID:
        await admin_panel_menu(update, context)
        return ADMIN_PANEL
    else:
        await start(update, context) # Or some other default behavior
        return MAIN_MENU

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    message_text = update.message.text

    if message_text == "Назад":
        await start(update, context)
        return MAIN_MENU

    await update.message.reply_text("⏳ Генерирую ответ...")
    logging.info(f"Message '{message_text}' from {user.full_name} ({user.id})")

    history = get_user_history(user.id)
    history.append({"role": "user", "content": message_text})

    response_text = await generate_response(history)
    if response_text is None:
        await update.message.reply_text("Произошла ошибка при генерации ответа. Попробуйте позже.")
        return MAIN_MENU

    add_request(user.id, message_text, response_text)
    await update.message.reply_text(response_text)
    return TYPING_REPLY

async def admin_panel_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_count = get_user_count()
    admin_menu_keyboard = [    [KeyboardButton("Посмотреть историю пользователя")],
    [KeyboardButton("Назад")],
]
    await update.message.reply_text(
        f"**Панель администратора**\n\nВсего пользователей: {user_count}",
        reply_markup=ReplyKeyboardMarkup(admin_menu_keyboard, resize_keyboard=True),
        parse_mode='Markdown'
    )

async def admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Посмотреть историю пользователя":
        users = get_all_users()
        user_buttons = [[KeyboardButton(f"{user[1]} ({user[0]})_history")] for user in users]
        user_buttons.append([KeyboardButton("Назад")])
        await update.message.reply_text(
            "Выбери пользователя:",
            reply_markup=ReplyKeyboardMarkup(user_buttons, resize_keyboard=True)
        )
        return VIEW_USER_HISTORY
    elif text == "Назад":
        await start(update, context)
        return MAIN_MENU
    return ADMIN_PANEL

async def view_user_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text.endswith("_history"):
        try:
            user_id = int(text.split(' (')[1].split(')')[0])
            history = get_user_history(user_id, limit=20)
            if not history:
                await update.message.reply_text("История сообщений пуста.")
            else:
                history_text = ""
                for msg in history:
                    history_text += f"*{msg['role'].capitalize()}*: {msg['content']}\n\n"
                await update.message.reply_text(history_text, parse_mode='Markdown')
        except (IndexError, ValueError):
            await update.message.reply_text("Неверный формат. Пожалуйста, выберите пользователя из списка.")
    elif text == "Назад":
        await admin_panel_menu(update, context)
        return ADMIN_PANEL
    return VIEW_USER_HISTORY

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("До свидания!")
    return ConversationHandler.END