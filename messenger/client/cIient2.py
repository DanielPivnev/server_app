import argparse
import sys
import time
import logging
from threading import Thread

import messenger.logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket

from messenger.common.errors import MissingArgument
from messenger.common.settings import DEFAULT_PORT, ACTION, ACCOUNT_NAME, TIME, USER, RESPONSE, PRESENCE, ERROR, \
    DEFAULT_IP_ADDR, HTTP_200_OK, ALERT, HTTP_400_BAD_REQUEST, CLIENT_LOG_NAME, MESSAGE, MESSAGE_TEXT, SENDER, \
    DESTINATION, EXIT
from messenger.common.utils import Courier
from messenger.common.decos import log

logger = logging.getLogger(CLIENT_LOG_NAME)


@log
def message_from_server(msg):
    if ACTION in msg and msg[ACTION] == MESSAGE and SENDER in msg and msg[SENDER] and MESSAGE_TEXT in msg and \
            msg[MESSAGE_TEXT]:
        print(f'\nReceived message from {msg[SENDER]}: \n{msg[MESSAGE_TEXT]}')
    else:
        raise ValueError


@log
def get_message(account_name='Guest'):
    receiver = input('Enter the receiver: ')
    while receiver == '':
        receiver = input('Enter the receiver: ')

    message = input('Enter the message: ')
    while message == '':
        message = input('Enter the message: ')

    message_dict = {
        ACTION: MESSAGE,
        DESTINATION: receiver,
        TIME: time.time(),
        SENDER: account_name,
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
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def process_answer(msg):
    if RESPONSE in msg and ALERT in msg and msg[RESPONSE] == HTTP_200_OK:
        return f'{msg[RESPONSE]} {msg[ALERT]}'
    elif RESPONSE in msg and ERROR in msg and msg[RESPONSE] == HTTP_400_BAD_REQUEST:
        return f'{msg[RESPONSE]} {msg[ERROR]}'
    else:
        raise ValueError


@log
def recv_message(courier, client):
    while True:
        try:
            message_from_server(courier.receive(client))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
            logger.error(e)
            sys.exit()
        except ValueError as e:
            logger.error(e)
        except OSError:
            logger.info(f'Client {client} left the messenger.')


@log
def send_message(courier, client, username):
    while True:
        try:
            cmd = input('Please enter a command: ')
            if cmd == 'message':
                courier.send(client, get_message(username))
            elif cmd == 'help':
                print_help()
            elif cmd == 'exit':
                courier.send(client, create_exit_message(username))
                sys.exit()
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as e:
            logger.error(e)
        except ValueError as e:
            logger.error(e)
        except OSError:
            logger.info(f'Client {client} left the messenger.')


@log
def print_help():
    print('Supported commands:')
    print('message - send message. Recipient and message are required.')
    print('help - print all commands')
    print('exit - exit messenger')


@log
def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-username', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    username = namespace.username

    return username


def main():
    courier = Courier()

    with socket(AF_INET, SOCK_STREAM) as client:
        try:
            client.connect((DEFAULT_IP_ADDR, DEFAULT_PORT))

            username = argument_parser()
            while username == '':
                username = input('Please enter an username: ')

            presence_message = create_presence(username)
            courier.send(client, presence_message)
            answer = courier.receive(client)

            response = process_answer(answer)

            logger.info(f'{response}')

        except ValueError as e:
            logger.error(e)
        except MissingArgument as e:
            logger.error(e)
            sys.exit(1)
        except ConnectionRefusedError as e:
            logger.critical(e)
            sys.exit(1)
        else:
            recv_thread = Thread(target=recv_message, name='receive thread', args=(courier, client))
            send_thread = Thread(target=send_message, name='send thread', args=(courier, client, username))

            recv_thread.daemon = True
            send_thread.daemon = True

            recv_thread.start()
            send_thread.start()

            while recv_thread.is_alive() and send_thread.is_alive():
                pass


if __name__ == '__main__':
    main()
