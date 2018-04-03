import random

chat_name_examples = ['hello-it-dev', 'hello-it-qa',
                      'hello-it-web', 'hello-it-devops',
                      'hello-it-hr', 'hello-it-dev-spring']


def welcome_message():
    return 'Welcome to Hello Father Bot!'


def logged_message():
    return 'Welcome again to Hello Father Bot!'


def help_message():
    return 'I can help you create chats under @hello_community platform.\n\n' + \
           'You can control me by sending these commands:\n\n' + \
           '/newchat - create a new chat\n' + \
           '/help    - display this message\n'


def new_chat_message():
    return 'Alright, a new chat. ' + \
           'How are we going to call it? ' + \
           'Please follow next convention: ^hello(-[a-z]+)+$\n' + \
           'Example: ' + random.choice(chat_name_examples)


def chat_name_mistake_message():
    return 'Chat name does not correspond to naming convention: ^hello(-[a-z]+)+$\n' + \
           'Example: ' + random.choice(chat_name_examples)


def chat_created_by_link_message(link):
    return 'Done! Congratulations on our new chat. You will find it at ' + link
