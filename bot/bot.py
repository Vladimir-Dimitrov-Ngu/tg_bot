import os
import logging
from allbooks import get_all_books
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import message_text


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    exit("Please specify telegram-bot token environment variable")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message_text.GREETINGS
    )


async def all_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("all books")
    all_books_chunks = await get_all_books(chunk_size=50)
    for chunk in all_books_chunks:
        response = "\n".join([book.name for book in chunk])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message_text.HELP
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    all_books_handler = CommandHandler("all_books", all_books)
    application.add_handler(all_books_handler)

    application.run_polling()
