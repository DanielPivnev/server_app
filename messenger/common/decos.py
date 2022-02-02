import logging
import inspect
import sys

import messenger.logs.client_log_config
import messenger.logs.server_log_config


if sys.argv[0].find('cIient') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')


def log(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами: {args}, {kwargs}. '
                     f'Вызов из модуля: {func.__module__}. '
                     f'Вызов из функции: {inspect.stack()[1][3]}. '
                     f'Возврат: {response}.', stacklevel=2)

        return response

    return wrapper

