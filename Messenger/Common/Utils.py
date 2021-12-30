import json

from Messenger.Common.Settings import DEFAULT_ENCODING, DEFAULT_MAX_PACKAGE_LENGTH


def send(client, message):
    message = json.dumps(message)
    message = message.encode(DEFAULT_ENCODING)
    client.send(message)


def receive(client):
    message = client.recv(DEFAULT_MAX_PACKAGE_LENGTH)

    message = message.decode(DEFAULT_ENCODING)
    message = json.loads(message)

    return message
