import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

load_dotenv()

secret_token = os.getenv('TOKEN')

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL).json()
    except ConnectionError:
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url).json()

    random_cat_url = response[0].get('url')
    return random_cat_url


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    button = ReplyKeyboardMarkup([['/new_cat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        reply_markup=button
        )
    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('new_cat', new_cat))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
