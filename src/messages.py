def help_message():
    return 'I can help you create chats under @hello_community platform.\n\n' + \
           'You can control me by sending these commands:\n\n' + \
           '/newchat - create a new chat\n'


def new_chat_message():
    return 'Alright, a new chat. ' + \
           'How are we going to call it? ' + \
           'Please follow next convention: ^hello(-[a-z]+)+$'


def chat_name_mistake_message():
    return 'Chat name does not correspond to naming convention: ^hello(-[a-z]+)+$\n' + \
           'Example: hello-it-dev'


def chat_created_by_link_message(link):
    return 'Done! Congratulations on our new chat. You will find it at t.me/' + link
