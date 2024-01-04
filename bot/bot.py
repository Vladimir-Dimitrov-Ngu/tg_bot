import os
import logging
from allbooks import (
    get_all_books,
    get_allready_all_books,
    get_now_books,
    get_non_started_books,
    get_books_by_numbers,
)
from votings import actual_voting_id, save_vote
import config
from datetime import datetime
import telegram
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import message_text
import re


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
        response += (
            f"{index}. {book.name} читали c {book.read_start} до {book.read_finish}"
            + "\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now_read_books = await get_now_books()
    response = "Сейчас мы читаем:\n\n"
    just_one_book = len(now_read_books) == 1
    for index, book in enumerate(now_read_books, 1):
        response += (
            f"{str(index) + '. ' if not just_one_book else ''}{book.name} читаем c {book.read_start} до {book.read_finish}"
            + "\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await actual_voting_id() is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.NO_ACTUAL_VOTING,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
        return

    categories_with_books = await get_non_started_books()
    index = 1
    for category in categories_with_books:
        response = "<b>" + category.name + "</b>\n\n"
        for book in category.books:
            response += f"{index}. {book.name}" + "\n"
            index += 1
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text.VOTE,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


async def vote_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await actual_voting_id() is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.NO_ACTUAL_VOTING,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
        return

    user_message = update.message.text
    numbers = re.findall(r"\d+", user_message)
    if len(tuple(set(map(int, numbers)))) != config.VOTE_ELEMENTS_COUNT:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.VOTE_PROCESS_INCORRECT_INPUT,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
        return

    books = await get_books_by_numbers(numbers)
    if len(books) != config.VOTE_ELEMENTS_COUNT:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.VOTE_PROCESS_INCORRECT_BOOKS,
        )
        return
    await save_vote(update.effective_user.id, books)
    response = f"Ура, ты выбрал {config.VOTE_ELEMENTS_COUNT} книги:\n\n"
    for index, book in enumerate(books, 1):
        response += str(index) + ". " + book.name + "\n"
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

    now_handler = CommandHandler("now", now)
    application.add_handler(now_handler)

    vote_handler = CommandHandler("vote", vote)
    application.add_handler(vote_handler)

    vote_process_hander = MessageHandler(
        filters.TEXT & (~filters.COMMAND), vote_process
    )
    application.add_handler(vote_process_hander)

    application.run_polling()
