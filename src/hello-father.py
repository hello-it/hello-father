# -*- coding: utf-8 -*-

import os
import sys
from messages import *
from utils import *

from telebot import TeleBot

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import token

bot = TeleBot(token)

create_context = {}


@bot.message_handler(commands=['login', 'start', 'signin', 'signup'])
def start(request):
    def process(message):
        user_id = message.chat.id
        create_context[user_id] = create_empty_context()
        #bot.send_message(user_id, help_message())

    process(request)


@bot.message_handler(commands=['newchat'])
def new_chat(request):
    def process(message):
        user_id = message.chat.id
        create_context[user_id]['open'] = True
        bot.send_message(user_id, new_chat_message())

    start(request)
    process(request)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def text(request):
    def process(message):
        user_id = message.chat.id
        if create_context[user_id]['open']:
            chat_name = message.text
            if is_valid_chat_name(chat_name):
                create_context[user_id]['chat_name'] = chat_name
                create_context[user_id]['open'] = False

                bot.send_message(user_id, chat_created_by_link_message(convert_chat_name_to_link(chat_name)))
            else:
                bot.send_message(user_id, chat_name_mistake_message())
        else:
            help(message)

    process(request)


@bot.message_handler(commands=['help'])
def help(request):
    def process(message):
        user_id = message.chat.id
        bot.send_message(user_id, help_message())

    start(request)
    process(request)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except BaseException:
        print('Connection refused')
