import logging
from logging import handlers


fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

client_handler = handlers.TimedRotatingFileHandler('client.log', 'midnight', 1, utc=False)
client_handler.setFormatter(fmt)
client_handler.setLevel(logging.INFO)

log = logging.getLogger('client')

log.addHandler(client_handler)
