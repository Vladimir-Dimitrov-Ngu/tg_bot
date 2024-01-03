import os
import logging
from allbooks import get_all_books, get_allready_all_books
import config
from datetime import datetime
import telegram
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
    categories_with_books = await get_all_books()
    for category in categories_with_books:
        response = "<b>" + category.name + "</b>\n\n"
        for index, book in enumerate(category.books, 1):
            response += f"{index}. {book.name}" + "\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode=telegram.constants.ParseMode.HTML,
        )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=message_text.HELP
    )


async def allready(update: Update, context: ContextTypes.DEFAULT_TYPE):
    allready_read_books = await get_allready_all_books()
    response = "Прочитанные книги:\n\n"
    for index, book in enumerate(allready_read_books, 1):
        read_start, read_finish = map(lambda date: datetime.strptime(date, '%Y-%m-%d'), [book.read_start, book.read_finish])
        read_start, read_finish = map(lambda date: date.strftime(config.DATE_FORMAT), [read_start, read_finish])
        response += (
            f"{index}. {book.name} читали c {read_start} до {read_finish}"
            + "\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    all_books_handler = CommandHandler("allbooks", all_books)
    application.add_handler(all_books_handler)

    allready_handler = CommandHandler("allready", allready)
    application.add_handler(allready_handler)

    application.run_polling()
