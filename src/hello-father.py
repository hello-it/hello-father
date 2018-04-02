# -*- coding: utf-8 -*-

import os
import re
import sys
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
    bot.send_message(message.chat.id,
                     'Alright, a new chat. ' +
                     'How are we going to call it? ' +
                     'Please follow next convention: ^hello(-[a-z]+)+$')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def lean(message):
    if create_context['open']:
        chat_name = message.text
        if is_valid_chat_name(chat_name):
            create_context['chat_name'] = chat_name
            create_context['open'] = False

            bot.send_message(message.chat.id,
                             'Done! Congratulations on our new chat. You will find it at t.me/' +
                             convert_chat_name_to_link(chat_name))
        else:
            bot.send_message(message.chat.id,
                             'Chat name does not correspond to naming convention: ^hello(-[a-z]+)+$\n' +
                             'Example: hello-it-dev')
    else:
        help(message)


def is_valid_chat_name(name):
    return re.match(r'^hello(-[a-z]+)+$', name)


def convert_chat_name_to_link(name):
    return name.replace('-', '_')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'I can help you create chats under @hello_community platform.\n\n' +
                     'You can control me by sending these commands:\n\n' +
                     '/newchat - create a new chat\n')


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except BaseException:
        print 'Connection refused'
