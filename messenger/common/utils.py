import json

from messenger.common.settings import DEFAULT_ENCODING, DEFAULT_MAX_PACKAGE_LENGTH
from decos import log


class Courier:
    def __init__(self, log_name):
        self.log_name = log_name

    def send(self, sock, message):
        @log(self.log_name)
        def send2(socket, msg):
            msg = json.dumps(msg)
            msg = msg.encode(DEFAULT_ENCODING)
            socket.send(msg)

        send2(sock, message)

    def receive(self, socket):
        @log(self.log_name)
        def receive2(sock):
            message = sock.recv(DEFAULT_MAX_PACKAGE_LENGTH)

            message = message.decode(DEFAULT_ENCODING)
            message = json.loads(message)

            return message

        return receive2(socket)
