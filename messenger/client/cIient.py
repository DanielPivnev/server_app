import argparse
import sys
import time
import logging
import messenger.logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.errors import MissingArgument, ClientExit
from messenger.common.settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDR, HTTP_200_OK, ALERT, HTTP_400_BAD_REQUEST, CLIENT_LOG_NAME, MESSAGE, MESSAGE_TEXT, SENDER
from messenger.common.utils import Courier
from messenger.common.decos import log

logger = logging.getLogger(CLIENT_LOG_NAME)


@log
def message_from_server(msg):
    if ACTION in msg and msg[ACTION] == MESSAGE and SENDER in msg and msg[SENDER] and MESSAGE_TEXT in msg and \
            msg[MESSAGE_TEXT]:
        print(msg[MESSAGE_TEXT])
    else:
        raise ValueError


@log
def get_message(client, account_name='Guest'):
    message = input('Enter msg or "!!!" to exit: ')

    if message == '!!!':
        raise ClientExit()

    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }

    return message_dict


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


@log
def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    client_mode = namespace.mode

    return client_mode


def main():
    courier = Courier()

    with socket(AF_INET, SOCK_STREAM) as client:
        try:
            client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

            presence_message = create_presence()
            courier.send(client, presence_message)
            answer = courier.receive(client)

            response = process_answer(answer)

            logger.info(f'{response}')

            mode = argument_parser()
            if not mode:
                raise MissingArgument('-m or --mode')

        except ValueError as e:
            logger.error(e)
        except MissingArgument as e:
            logger.error(e)
            sys.exit(1)
        except ConnectionRefusedError as e:
            logger.critical(e)
            sys.exit(1)
        else:
            while True:
                try:
                    if mode == 'send':
                        courier.send(client, get_message(client))
                    elif mode == 'listen':
                        message_from_server(courier.receive(client))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
                    logger.error(e)
                except ValueError as e:
                    logger.error(e)
                except ClientExit as e:
                    client.close()
                    logger.info(e)


if __name__ == '__main__':
    main()
