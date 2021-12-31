import time
from socket import AF_INET, SOCK_STREAM, socket

from Messenger.Common.Settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, PRESENCE, DEFAULT_IP_ADDR
from Messenger.Common.Utils import receive, send


def create_presence(account_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return response


def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

    presence_message = create_presence()
    send(client, presence_message)
    answer = receive(client)

    print(answer)
    input('...')
    client.close()


if __name__ == '__main__':
    main()
