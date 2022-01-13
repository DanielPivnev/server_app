import time
from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.settings import DEFAULT_PORT, DEFAULT_LISTEN_ADDR, DEFAULT_QUEUE_LENGTH, ACTION, ACCOUNT_NAME, \
    TIME, USER, RESPONSE, PRESENCE, ERROR, DEFAULT_IP_ADDR, HTTP_200_OK, ALERT
from messenger.common.utils import receive, send


def create_presence(account_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return response


def process_answer(msg):
    if RESPONSE in msg and msg[RESPONSE] == HTTP_200_OK:
        return f'{msg[RESPONSE]} {msg[ALERT]}'
    elif RESPONSE in msg and ERROR in msg:
        return f'{msg[RESPONSE]} {msg[ERROR]}'
    else:
        raise ValueError


def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

    presence_message = create_presence()
    send(client, presence_message)
    answer = receive(client)

    try:
        response = process_answer(answer)
        print(response)
    except ValueError as e:
        print(e)

    client.close()


if __name__ == '__main__':
    main()
