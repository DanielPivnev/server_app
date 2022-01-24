import json
import logging

from messenger.common.settings import DEFAULT_ENCODING, DEFAULT_MAX_PACKAGE_LENGTH


def send(sock, message, log_name, to_addr='server'):
    message = json.dumps(message)
    message = message.encode(DEFAULT_ENCODING)
    sock.send(message)
    log = logging.getLogger(log_name)
    log.info(f'message "{message}" sent to {to_addr}')


def receive(sock, log_name, to_addr='server'):
    message = sock.recv(DEFAULT_MAX_PACKAGE_LENGTH)

    message = message.decode(DEFAULT_ENCODING)
    message = json.loads(message)

    log = logging.getLogger(log_name)
    log.info(f'message "{message}" received from {to_addr}')

    return message
