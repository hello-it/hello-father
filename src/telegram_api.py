# -*- coding: utf-8 -*-

import sys
import os

from utils import convert_chat_name_to_link

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'resources'))
from config import api_id, api_hash

from telethon import TelegramClient
from telethon.tl.functions.channels import *
from telethon.tl.types import *

client = TelegramClient('session', api_id, api_hash)
client.start()


def create_telegram_chat(chat_name, creator_id):
    print('New chat name: ' + str(chat_name))

    new_chat_id = create_chat(chat_name)
    print('New chat id: ' + str(new_chat_id))

    enable_public_invites(new_chat_id)
    print('Public invites have enabled')

    new_chat_link = create_chat_link(new_chat_id, chat_name)
    print('New chat link: ' + str(new_chat_link))

    invite_and_add_admins(new_chat_id, creator_id)
    print('Admins have invited and upgraded')

    return new_chat_link


def create_chat(chat_name):
    return client(CreateChannelRequest(
        title=chat_name,
        about='Мы обсуждаем ' + chat_name[chat_name.rfind('-') + 1:].upper() + ' темы',
        broadcast=True,
        megagroup=True
    )).updates[1].channel_id


def enable_public_invites(new_chat_id):
    client(ToggleInvitesRequest(
        channel=client.get_entity(new_chat_id),
        enabled=True
    ))


def create_chat_link(chat_id, chat_name):
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


def invite_and_add_admins(chat_id, creator_id):
    client(InviteToChannelRequest(
        channel=client.get_entity(chat_id),
        users=[client.get_entity(63756324), client.get_entity(202319269)]
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

    # Creator
    client(EditAdminRequest(
        channel=client.get_entity(chat_id),
        user_id=client.get_entity(creator_id),
        admin_rights=full_rights
    ))

    # Vadim Kiselev
    client(EditAdminRequest(
        channel=client.get_entity(chat_id),
        user_id=client.get_entity(63756324),
        admin_rights=full_rights
    ))

    # Alexander Sharov
    client(EditAdminRequest(
        channel=client.get_entity(chat_id),
        user_id=client.get_entity(202319269),
        admin_rights=full_rights
    ))