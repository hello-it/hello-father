import re


def create_empty_context():
    return {
        'open': False,
        'phone_number': False,
        'access_code': False
    }


def is_valid_chat_name(name):
    return re.match(r'^hello(-[a-z]+)+$', name)


def convert_chat_name_to_link(name):
    return name.replace('-', '_')


def retrieve_name_from_message(message):
    try:
        return message.chat.first_name + ' ' + message.chat.last_name
    except BaseException:
        return message.chat.username
