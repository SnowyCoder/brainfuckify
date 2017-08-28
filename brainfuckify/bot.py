import telegram
import os
import logging

from telegram import *
from telegram.ext import *
from core import encode

URL = 'https://brainfuckify.herokuapp.com/'
TOKEN = os.environ['TOKEN']
PORT = int(os.environ['PORT'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(TOKEN)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, write anything and I'll brainfuck it")


def message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=encode(update.message.text))


def inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Brainfuckify',
            description='Brainfuck encoded text',
            input_message_content=InputTextMessageContent(encode(query.upper()))
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, message))
dispatcher.add_handler(InlineQueryHandler(inline))


def on_error(bot, update, error):
    logging.exception("Telegram error")


dispatcher.add_error_handler(callback=on_error)


updater.start_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN
)

updater.bot.set_webhook(URL + TOKEN)

updater.idle()
