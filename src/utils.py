import re


def create_empty_context():
    return {
        'open': False,
        'chat_name': None
    }


def is_valid_chat_name(name):
    return re.match(r'^hello(-[a-z]+)+$', name)


def convert_chat_name_to_link(name):
    return name.replace('-', '_')
