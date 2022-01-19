import logging
from logging import handlers


fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

server_handler = handlers.TimedRotatingFileHandler('server.log', 'midnight', 1, utc=False)
server_handler.setFormatter(fmt)
server_handler.setLevel(logging.INFO)

log = logging.getLogger('server')

log.addHandler(server_handler)
