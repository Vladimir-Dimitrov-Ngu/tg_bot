import os
import logging
import config
import re
import matplotlib.pyplot as plt
from io import BytesIO
from telegram import (
    Update,
    InputFile,
    constants,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from allbooks import (
    get_all_books,
    get_allready_all_books,
    get_now_books,
    get_non_started_books,
    get_books_by_numbers,
    build_category_with_books_string,
)
from votings import get_actual_voting, save_vote, get_leaders
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
            parse_mode=constants.ParseMode.HTML,
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
            f"{str(index) + '. ' if not just_one_book else ''}{book.name} \
                читаем c {book.read_start} до {book.read_finish}"
            + "\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await get_actual_voting() is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.NO_ACTUAL_VOTING,
            parse_mode=constants.ParseMode.HTML,
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
            parse_mode=constants.ParseMode.HTML,
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text.VOTE,
        parse_mode=constants.ParseMode.HTML,
    )


async def vote_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await get_actual_voting() is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.NO_ACTUAL_VOTING,
            parse_mode=constants.ParseMode.HTML,
        )
        return

    user_message = update.message.text
    numbers = re.findall(r"\d+", user_message)
    if len(tuple(set(map(int, numbers)))) != config.VOTE_ELEMENTS_COUNT:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text.VOTE_PROCESS_INCORRECT_INPUT,
            parse_mode=constants.ParseMode.HTML,
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
    books_formatted = []
    for index, book in enumerate(books, 1):
        books_formatted.append(str(index) + ". " + book.name)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text.SUCCESS_VOTE.format(books="\n".join(books_formatted)),
    )
    return


async def vote_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaders = await get_leaders()
    if leaders is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=message_text.NO_VOTE_RESULTS
        )
        return
    response = "Топ 5 книг голосования:\n\n"
    for index, book in enumerate(leaders.leaders, 1):
        response += f"{index}. {book.book_name}: {book.score}\n"
    response += f"Даты голосования: {leaders.vote_start} - {leaders.vote_finish}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return


async def vote_results_graph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaders = await get_leaders()
    if leaders is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=message_text.NO_VOTE_RESULTS
        )
        return
    books_scores = {book.book_name: book.score for book in leaders.leaders}
    sorted_books_scores = dict(
        sorted(books_scores.items(), key=lambda item: item[1], reverse=False)
    )
    books_name = list(sorted_books_scores.keys())
    books_scores = list(sorted_books_scores.values())
    plt.figure(figsize=(5, 5))
    plt.barh(books_name, books_scores, color="skyblue")
    plt.xlabel("Голоса")
    plt.title("Результаты голосования")
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
    buffer.seek(0)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=InputFile(buffer)
    )
    return


async def all_books_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories_with_books = list(await get_all_books())

    keyboard = [
        [
            InlineKeyboardButton("Предыдущая категория", callback_data="left"),
            InlineKeyboardButton("Следующая категория", callback_data="right"),
        ],
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        build_category_with_books_string(categories_with_books[0]),
        reply_markup=reply_keyboard,
        parse_mode=constants.ParseMode.HTML,
    )
    return


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "right":
        await query.edit_message_text(text=f"Дружок-пирожок, ты выбрал: {query.data}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    all_books_handler = CommandHandler("allbooks", all_books)
    application.add_handler(all_books_handler)

    all_books_handler_2 = CommandHandler("allbooks2", all_books_2)
    application.add_handler(all_books_handler_2)
    application.add_handler(CallbackQueryHandler(button))

    allready_handler = CommandHandler("allready", allready)
    application.add_handler(allready_handler)

    now_handler = CommandHandler("now", now)
    application.add_handler(now_handler)

    vote_handler = CommandHandler("vote", vote)
    application.add_handler(vote_handler)

    vote_results_handler = CommandHandler("voteresults", vote_results)
    application.add_handler(vote_results_handler)

    vote_results_graph_handler = CommandHandler("voteresultsgraph", vote_results_graph)
    application.add_handler(vote_results_graph_handler)

    vote_process_hander = MessageHandler(
        filters.TEXT & (~filters.COMMAND), vote_process
    )
    application.add_handler(vote_process_hander)

    application.run_polling()
