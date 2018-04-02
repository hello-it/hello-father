# -*- coding: utf-8 -*-

import sys
import time

from messages import *
from utils import *

from telebot import TeleBot
from telethon import TelegramClient
from telethon.tl.functions.channels import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import *


bot = TeleBot(token)
client = TelegramClient('session', api_id, api_hash)
client.start()

create_context = {}


@bot.message_handler(commands=['login', 'start', 'signin', 'signup'])
def start(request):
    def process(message):
        user_id = message.chat.id
        create_context[user_id] = create_empty_context()

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
        if create_context[user_id] and create_context[user_id]['open']:
            chat_name = message.text
            if is_valid_chat_name(chat_name):
                create_context[user_id]['chat_name'] = chat_name
                create_context[user_id]['open'] = False

                response = client(CreateChannelRequest(
                    title=chat_name,
                    about='Мы обсуждаем ' + chat_name[chat_name.rfind('-') + 1:].upper() +  ' темы',
                    broadcast=True,
                    megagroup=True
                ))

                time.sleep(1000)

                new_chat_id = response.updates[1].channel_id

                client(ToggleInvitesRequest(
                    channel=client.get_entity(new_chat_id),
                    enabled=True
                ))

                time.sleep(1000)

                new_chat_link = 'https://t.me/' + convert_chat_name_to_link(chat_name)

                try:
                    client(UpdateUsernameRequest(
                        channel=client.get_entity(new_chat_id),
                        username=convert_chat_name_to_link(chat_name)
                    ))
                except BaseException:
                    time.sleep(1000)
                    new_chat_link = client(ExportInviteRequest(
                        channel=client.get_entity(new_chat_id)
                    )).link

                # client(EditAdminRequest(
                #     channel=client.get_entity(new_chat_id),
                #     user_id=client.get_entity(message.chat.id),
                #     admin_rights=TypeChannelAdminRights(True, True, True, True, True, True, True, True, True)
                # ))

                bot.send_message(user_id, chat_created_by_link_message(new_chat_link))
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
