# -*- coding: utf-8 -*-

import sys
import os

from messages import chat_created_by_link_message, chat_name_mistake_message, \
    help_message, new_chat_message, welcome_message, logged_message

from telegram_api import create_telegram_chat, telegram_login, \
    save_phone_number, save_access_code, telegram_start

from utils import is_valid_chat_name, create_empty_context, retrieve_name_from_message

from messages import enter_phone_number_message, enter_access_code_message, successfully_logged_in_message

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import token

from telebot import TeleBot

bot = TeleBot(token)
context = {}


# Endpoints
@bot.message_handler(commands=['login', 'start', 'signin', 'signup'])
def welcome(request):
    log_processor(request)
    welcome_processor(request)
    start_processor(request)


@bot.message_handler(commands=['newchat'])
def new_chat(request):
    log_processor(request)
    start_processor(request)
    new_chat_processor(request)


@bot.message_handler(commands=['help'])
def help(request):
    log_processor(request)
    start_processor(request)
    help_processor(request)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def text(request):
    log_processor(request)
    start_processor(request)
    text_processor(request)


# Processors
def log_processor(message):
    print('[' + str(message.chat.id) + '] ' + retrieve_name_from_message(message) + ': ' + message.text)


def welcome_processor(message):
    user_id = message.chat.id
    if user_id not in context:
        bot.send_message(message.chat.id, welcome_message())
    else:
        bot.send_message(message.chat.id, logged_message())


def start_processor(message):
    user_id = message.chat.id
    if user_id not in context:
        context[user_id] = create_empty_context()

        telegram_login(user_id)
        bot.send_message(user_id, enter_phone_number_message())


def help_processor(message):
    user_id = message.chat.id
    bot.send_message(user_id, help_message())


def new_chat_processor(message):
    user_id = message.chat.id
    context[user_id]['open'] = True
    bot.send_message(user_id, new_chat_message())


def text_processor(message):
    user_id = message.chat.id
    if not context[user_id]['phone_number']:
        save_phone_number(user_id, message.text)
        context[user_id]['phone_number'] = True

        bot.send_message(user_id, enter_access_code_message())
    elif not context[user_id]['access_code']:
        save_access_code(user_id, message.text)
        context[user_id]['access_code'] = True
        telegram_start(user_id)

        bot.send_message(user_id, successfully_logged_in_message(retrieve_name_from_message(message)))
    elif context[user_id]['open']:
        chat_name = message.text
        if is_valid_chat_name(chat_name):
            context[user_id]['open'] = False

            telegram_link = create_telegram_chat(chat_name, message.chat.id)

            bot.send_message(user_id, chat_created_by_link_message(telegram_link))
        else:
            bot.send_message(user_id, chat_name_mistake_message())
    else:
        help_processor(message)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except BaseException as exception:
        print('Connection refused')
        print(exception)
