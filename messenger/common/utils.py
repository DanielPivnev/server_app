import json

from messenger.common.settings import DEFAULT_ENCODING, DEFAULT_MAX_PACKAGE_LENGTH
from messenger.common.decos import log


class Courier:
    @log
    def send(self, sock, msg):
        msg = json.dumps(msg)
        msg = msg.encode(DEFAULT_ENCODING)
        sock.send(msg)

    @log
    def receive(self, sock):
        message = sock.recv(DEFAULT_MAX_PACKAGE_LENGTH)

        message = message.decode(DEFAULT_ENCODING)
        message = json.loads(message)

        return message
