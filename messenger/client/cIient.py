import time
import logging
import messenger.logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDR, HTTP_200_OK, ALERT, HTTP_400_BAD_REQUEST, CLIENT_LOG_NAME
from messenger.common.utils import Courier
from messenger.common.decos import log


@log
def create_presence(account_name='Guest'):
    response = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return response


@log
def process_answer(msg):
    if RESPONSE in msg and ALERT in msg and msg[RESPONSE] == HTTP_200_OK:
        return f'{msg[RESPONSE]} {msg[ALERT]}'
    elif RESPONSE in msg and ERROR in msg and msg[RESPONSE] == HTTP_400_BAD_REQUEST:
        return f'{msg[RESPONSE]} {msg[ERROR]}'
    else:
        raise ValueError


def main():
    courier = Courier(CLIENT_LOG_NAME)
    logger = logging.getLogger(CLIENT_LOG_NAME)

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

    try:
        presence_message = create_presence()
        courier.send(client, presence_message)
        answer = courier.receive(client)

        response = process_answer(answer)

        logger.info(f'{response}')
    except ValueError as e:
        logger.error(e)

    client.close()


if __name__ == '__main__':
    main()
