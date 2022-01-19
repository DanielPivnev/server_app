import logging
from logging import handlers

from messenger.common.settings import CLIENT_LOG_NAME


def create_client_log():
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

    client_handler = handlers.TimedRotatingFileHandler(f'{CLIENT_LOG_NAME}.log', 'midnight', 1, utc=False)
    client_handler.setFormatter(fmt)
    client_handler.setLevel(logging.DEBUG)

    log = logging.getLogger(CLIENT_LOG_NAME)

    log.addHandler(client_handler)
