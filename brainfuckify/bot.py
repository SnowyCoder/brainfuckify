import telegram
import os
import logging

from telegram import *
from telegram.ext import *

URL = 'https://brainfuckify.herokuapp.com/'
TOKEN = os.environ['TOKEN']
PORT = int(os.environ['PORT'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(TOKEN)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, message))
dispatcher.add_handler(InlineQueryHandler(inline))

updater.start_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN
)

updater.bot.set_webhook(URL + TOKEN)

updater.idle()
