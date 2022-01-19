from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.settings import DEFAULT_PORT, DEFAULT_LISTEN_ADDR, DEFAULT_QUEUE_LENGTH, ACTION, ACCOUNT_NAME, \
    TIME, USER, RESPONSE, PRESENCE, ERROR, ALERT
from messenger.common.utils import receive, send


def process_message(message):
    if ACTION in message and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest' \
            and message[ACTION] == PRESENCE:
        return {RESPONSE: 200, ALERT: 'OK'}
    return {RESPONSE: 400, ERROR: 'Bad Request'}


def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((DEFAULT_LISTEN_ADDR, DEFAULT_PORT))
    server.listen(DEFAULT_QUEUE_LENGTH)

    try:
        while True:
            client, addr = server.accept()
            message = receive(client)
            response = process_message(message)
            print(response)
            send(client, response)
    finally:
        server.close()


if __name__ == '__main__':
    main()
