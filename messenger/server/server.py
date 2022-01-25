import logging
from socket import AF_INET, SOCK_STREAM, socket

import messenger.logs.server_log_config
from messenger.common.settings import DEFAULT_PORT, DEFAULT_LISTEN_ADDR, DEFAULT_QUEUE_LENGTH, ACTION, ACCOUNT_NAME, \
    TIME, USER, RESPONSE, PRESENCE, ERROR, ALERT, SERVER_LOG_NAME
from messenger.common.utils import Courier
from messenger.common.decos import log

logger = logging.getLogger(SERVER_LOG_NAME)


@log
def process_message(message):
    if ACTION in message and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest' \
            and message[ACTION] == PRESENCE:
        response = {RESPONSE: 200, ALERT: 'OK'}

        return response
    response = {RESPONSE: 400, ERROR: 'Bad Request'}

    return response


def main():
    courier = Courier()

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((DEFAULT_LISTEN_ADDR, DEFAULT_PORT))
    server.listen(DEFAULT_QUEUE_LENGTH)

    try:
        while True:
            client, addr = server.accept()
            message = courier.receive(client)
            response = process_message(message)

            logger.info(f'{response}')

            courier.send(client, response)
    except Exception as e:
        logger.critical(e)
    finally:
        server.close()


if __name__ == '__main__':
    main()
