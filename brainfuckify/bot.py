import os
import logging
import string

from telegram import *
from telegram.ext import *
from telegram.utils.helpers import escape_markdown

from core import encode
from simulate import simulate

URL = 'https://brainfuckify.herokuapp.com/'
SRC_URL = 'https://github.com/SnowyCoder/brainfuckify'
TOKEN = os.environ['TOKEN']
PORT = int(os.environ['PORT'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(TOKEN)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello, write anything and I'll brainfuck it")


def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="author: @SnowyCoder")


def source(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="You can find the source here:\n" + SRC_URL)


def message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=encode(update.message.text))


def inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id='brainfuck',
            title='Brainfuckify',
            description='Brainfuck encoded text',
            input_message_content=InputTextMessageContent(encode(query))
        )
    )
    translate_success, translation, translate_iter = simulate(query)

    translation = ''.join(map(lambda x: '�' if x not in string.printable else x, translation))

    translation = 'Result: ' + translation
    results.append(
        InlineQueryResultArticle(
            id='translated',
            title='Decode',
            description='Brainfuck decoded text',
            input_message_content=InputTextMessageContent(escape_markdown(translation))
        )
    )

    bot.answer_inline_query(update.inline_query.id, results)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('source', source))
dispatcher.add_handler(MessageHandler(Filters.text, message))
dispatcher.add_handler(InlineQueryHandler(inline))


def on_error(bot, update, error):
    logging.exception("Telegram error")


dispatcher.add_error_handler(callback=on_error)

if __name__ == '__main__':
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )

    updater.bot.set_webhook(URL + TOKEN)

    updater.idle()
