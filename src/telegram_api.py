# -*- coding: utf-8 -*-

import sys
import os

from utils import convert_chat_name_to_link

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import api_id, api_hash

from telethon import TelegramClient
from telethon import utils
from telethon.tl.functions.channels import *
from telethon.errors.rpc_error_list import *
from telethon.tl.types import *

context = {}


def telegram_login(user_id):
    client = TelegramClient('session#' + str(user_id), api_id, api_hash)
    client.connect()
    context[user_id] = {
        'client': client,
        'phone_number': '',
        'access_code': ''
    }


def save_phone_number(user_id, phone_number):
    if user_id in context:
        data = context[user_id]
        client = data['client']
        context[user_id]['phone_number'] = phone_number
        client.send_code_request(phone_number)


def save_access_code(user_id, access_code):
    if user_id in context:
        context[user_id]['access_code'] = access_code


def telegram_start(user_id):
    if user_id in context:
        data = context[user_id]
        client = data['client']
        phone_number = data['phone_number']
        access_code = data['access_code'].replace('code', '')

        user = client.sign_in(phone=phone_number, code=access_code)
        print('Successfully logged in as ' + utils.get_display_name(user))


def create_telegram_chat(chat_name, creator_id):
    client = context[creator_id]['client']

    print('\nNew chat name: ' + str(chat_name))

    new_chat_id = create_chat(client, chat_name)
    print('New chat id: ' + str(new_chat_id))

    enable_public_invites(client, new_chat_id)
    print('Public invites have enabled')

    new_chat_link = create_chat_link(client, new_chat_id, chat_name)
    print('New chat link: ' + str(new_chat_link))

    invite_and_add_admins(client, new_chat_id)
    print('Admins have invited and upgraded\n')

    return new_chat_link


def create_chat(client, chat_name):
    return client(CreateChannelRequest(
        title=chat_name,
        about='Мы обсуждаем ' + chat_name[chat_name.rfind('-') + 1:].upper() + ' темы',
        broadcast=True,
        megagroup=True
    )).updates[1].channel_id


def enable_public_invites(client, new_chat_id):
    client(ToggleInvitesRequest(
        channel=client.get_entity(new_chat_id),
        enabled=True
    ))


def create_chat_link(client, chat_id, chat_name):
    converted_link = convert_chat_name_to_link(chat_name)
    new_chat_link = 'https://t.me/' + converted_link

    try:
        client(UpdateUsernameRequest(
            channel=client.get_entity(chat_id),
            username=converted_link
        ))
    except BaseException as exception:
        print(exception)
        new_chat_link = client(ExportInviteRequest(
            channel=client.get_entity(chat_id)
        )).link

    return new_chat_link


def invite_and_add_admins(client, chat_id):
    try:
        chat = client.get_entity(chat_id)

        vadim_username = '@vadimkiselev'
        vadim = client.get_entity(vadim_username)

        alex_username = '@kvendingoldo'
        alex = client.get_entity(alex_username)

        vadim_b_username = '@VBeskrovnov'

        client(InviteToChannelRequest(
            channel=chat,
            users=[vadim_username, alex_username, vadim_b_username]
        ))

        full_rights = ChannelAdminRights(
            post_messages=True,
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            invite_link=True,
            edit_messages=True
        )

        try:
            # Vadim Kiselev
            client(EditAdminRequest(
                channel=chat,
                user_id=vadim,
                admin_rights=full_rights
            ))
        except UserIdInvalidError as exception:
            print('Vadim Kiselev hasn\'t been provided to admin because of:')
            print(exception)

        try:
            # Alexander Sharov
            client(EditAdminRequest(
                channel=chat,
                user_id=alex,
                admin_rights=full_rights
            ))
        except UserIdInvalidError as exception:
            print('Alexander Sharov hasn\'t been provided to admin because of:')
            print(exception)

    except UserIdInvalidError as exception:
        print(exception)
