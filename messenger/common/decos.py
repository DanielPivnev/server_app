import logging
import inspect

import messenger.logs.client_log_config
import messenger.logs.server_log_config


def log(logger):
    def log_saver(func):
        def wrapper(*args, **kwargs):
            LOGGER = logging.getLogger(logger)

            response = func(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами: {args}, {kwargs}. '
                         f'Вызов из модуля: {func.__module__}. '
                         f'Вызов из функции: {inspect.stack()[1][3]}. '
                         f'Возврат: {response}.', stacklevel=2)

            return response

        return wrapper

    return log_saver
