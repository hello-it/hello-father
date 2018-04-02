# -*- coding: utf-8 -*-

import os
import sys
from messages import *
from utils import *

from telebot import TeleBot

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import token

bot = TeleBot(token)

create_context = {
    'open': False,
    'chat_name': None
}


@bot.message_handler(commands=['newchat'])
def new_chat(message):
    create_context['open'] = True
    bot.send_message(message.chat.id, new_chat_message())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def text(message):
    if create_context['open']:
        chat_name = message.text
        if is_valid_chat_name(chat_name):
            create_context['chat_name'] = chat_name
            create_context['open'] = False
            bot.send_message(message.chat.id, chat_created_by_link_message(convert_chat_name_to_link(chat_name)))
        else:
            bot.send_message(message.chat.id, chat_name_mistake_message())
    else:
        help(message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_message())


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except BaseException:
        print 'Connection refused'
