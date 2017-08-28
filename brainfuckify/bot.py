import telegram
import os
import logging

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


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, message))

updater.start_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN
)

updater.bot.set_webhook(URL + TOKEN)

updater.idle()
