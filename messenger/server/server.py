import logging
from socket import AF_INET, SOCK_STREAM, socket

import messenger.logs.server_log_config
from messenger.common.settings import DEFAULT_PORT, DEFAULT_LISTEN_ADDR, DEFAULT_QUEUE_LENGTH, ACTION, ACCOUNT_NAME, \
    TIME, USER, RESPONSE, PRESENCE, ERROR, ALERT, SERVER_LOG_NAME
from messenger.common.utils import receive, send


def process_message(message, log):
    if ACTION in message and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest' \
            and message[ACTION] == PRESENCE:
        response = {RESPONSE: 200, ALERT: 'OK'}

        log.debug(f'{response}')
        return response
    response = {RESPONSE: 400, ERROR: 'Bad Request'}

    log.debug(f'{response}')
    return response


def main():
    log = logging.getLogger(SERVER_LOG_NAME)

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((DEFAULT_LISTEN_ADDR, DEFAULT_PORT))
    server.listen(DEFAULT_QUEUE_LENGTH)

    try:
        while True:
            client, addr = server.accept()
            message = receive(client, SERVER_LOG_NAME)
            response = process_message(message, log)

            log.info(f'{response}')

            send(client, response, SERVER_LOG_NAME, addr)
    except Exception as e:
        log.critical(e)
    finally:
        server.close()


if __name__ == '__main__':
    main()
