import logging
from logging import handlers

from messenger.common.settings import SERVER_LOG_NAME


def create_server_log():
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

    server_handler = handlers.TimedRotatingFileHandler(f'{SERVER_LOG_NAME}.log', 'midnight', 1, utc=False)
    server_handler.setFormatter(fmt)
    server_handler.setLevel(logging.DEBUG)

    log = logging.getLogger(SERVER_LOG_NAME)

    log.addHandler(server_handler)
