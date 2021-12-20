"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import chardet

ARGS = [
    ['ping', 'yandex.ru'],
    ['ping', 'youtube.com']
]

# PING = subprocess.Popen(ARGS[0], stdout=subprocess.PIPE)
#
# for line in PING.stdout:
#     settings = chardet.detect(line)
#     line = line.decode(settings['encoding']).encode('utf-8')
#     print(line.decode('utf-8'))

PING = subprocess.Popen(ARGS[1], stdout=subprocess.PIPE)

for line in PING.stdout:
    settings = chardet.detect(line)
    line = line.decode(settings['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
