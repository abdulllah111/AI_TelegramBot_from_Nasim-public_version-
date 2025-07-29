from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, PicklePersistence
from src.config import BOT_TOKEN
from src.handlers.handlers import (
    start, main_menu, message_handler, admin_actions, view_user_history, done,
    MAIN_MENU, TYPING_REPLY, ADMIN_PANEL, VIEW_USER_HISTORY
)

def main() -> None:
    """Start the bot."""
    persistence = PicklePersistence(filepath="conversation_persistence")
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
            ADMIN_PANEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_actions)],
            VIEW_USER_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, view_user_history)],
        },
        fallbacks=[CommandHandler("done", done)],
        name="main_conversation",
        persistent=True,
        per_message=False
    )

    application.add_handler(conv_handler)

    application.run_polling()
