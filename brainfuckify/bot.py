import telegram
import os
import logging

from telegram.ext import Updater, CommandHandler

URL = 'https://brainfuckify.herokuapp.com/'
TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(TOKEN)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


dispatcher.add_handler(CommandHandler('start', start))


updater.start_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN
)

updater.bot.set_webhook(URL + TOKEN)

updater.idle()

