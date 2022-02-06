import logging
from socket import AF_INET, SOCK_STREAM, socket

import select

import messenger.logs.server_log_config
from messenger.common.settings import DEFAULT_PORT, DEFAULT_LISTEN_ADDR, DEFAULT_QUEUE_LENGTH, ACTION, ACCOUNT_NAME, \
    TIME, USER, RESPONSE, PRESENCE, ERROR, ALERT, SERVER_LOG_NAME, MESSAGE, MESSAGE_TEXT, EXIT, DESTINATION
from messenger.common.utils import Courier
from messenger.common.decos import log

logger = logging.getLogger(SERVER_LOG_NAME)


@log
def process_message(message):
    if ACTION in message and TIME in message and USER in message and message[USER][ACCOUNT_NAME] \
            and message[ACTION] == PRESENCE:
        return {ACCOUNT_NAME: message[USER][ACCOUNT_NAME], RESPONSE: 200, ALERT: 'OK'}

    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        return message

    elif ACTION in message and message[ACTION] == EXIT and TIME in message and MESSAGE_TEXT in message:
        return {ACTION: EXIT, ACCOUNT_NAME: message[ACCOUNT_NAME]}

    return {RESPONSE: 400, ERROR: 'Bad Request'}


def main():
    courier = Courier()

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((DEFAULT_LISTEN_ADDR, DEFAULT_PORT))
    server.listen(DEFAULT_QUEUE_LENGTH)
    server.settimeout(0.5)

    clients, messages, names = [], {}, {}

    while True:
        try:
            client, addr = server.accept()
        except OSError as e:
            pass
        else:
            clients.append(client)
            logger.info(f'Connection to {client} is created')

        recv_data, send_data, err_data = [], [], []

        try:
            if clients:
                recv_data, send_data, err_data = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data:
            for client in recv_data:
                try:
                    response = process_message(courier.receive(client))
                    if RESPONSE in response and response[RESPONSE] == 200:
                        names[client] = response[ACCOUNT_NAME]
                        del response[ACCOUNT_NAME]
                        courier.send(client, response)
                    elif RESPONSE in response and response[RESPONSE] == 400:
                        courier.send(client, response)
                    elif ACTION in response and response[ACTION] == EXIT:
                        del names[client]
                        clients.remove(client)
                        courier.send(client, response)
                    elif response[DESTINATION] in messages:
                        messages[response[DESTINATION]].append(response)
                    else:
                        messages[response[DESTINATION]] = [response]

                except (ConnectionAbortedError, ConnectionResetError):
                    logger.info(f'{client} has disconnected from the server')
                    clients.remove(client)

        if messages and send_data:
            for client in send_data:
                try:
                    for message in messages[names[client]]:
                        courier.send(client, message)
                        messages[names[client]].remove(message)
                except ConnectionAbortedError:
                    logger.info(f'{client} has disconnected from the server')
                    clients.remove(client)
                except KeyError:
                    pass


if __name__ == '__main__':
    main()
