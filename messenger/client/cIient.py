import time
import logging
import messenger.logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDR, HTTP_200_OK, ALERT, HTTP_400_BAD_REQUEST, CLIENT_LOG_NAME
from messenger.common.utils import receive, send


def create_presence(log, account_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    log.debug('created presence')

    return response


def process_answer(msg, log):
    if RESPONSE in msg and ALERT in msg and msg[RESPONSE] == HTTP_200_OK:
        log.debug(f'{msg[RESPONSE]} {msg[ALERT]}')
        return f'{msg[RESPONSE]} {msg[ALERT]}'
    elif RESPONSE in msg and ERROR in msg and msg[RESPONSE] == HTTP_400_BAD_REQUEST:
        log.debug(f'{msg[RESPONSE]} {msg[ERROR]}')
        return f'{msg[RESPONSE]} {msg[ERROR]}'
    else:
        raise ValueError


def main():
    log = logging.getLogger(CLIENT_LOG_NAME)

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

    try:
        presence_message = create_presence(log)
        send(client, presence_message, CLIENT_LOG_NAME)
        answer = receive(client, CLIENT_LOG_NAME)

        response = process_answer(answer, log)

        log.info(f'{response}')
    except ValueError as e:
        log.error(e)

    client.close()


if __name__ == '__main__':
    main()
