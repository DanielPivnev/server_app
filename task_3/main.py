"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml
from yaml import FullLoader

products = {
    'items': ['computer', 'printer', 'keyboard', 'mouse'],
    'items_price': {
        'computer': '200€-1000€',
        'keyboard': '5€-50€',
        'mouse': '4€-7€',
        'printer': '100€-300€',
    },
    'items_quantity': 4
}


def read_data():
    with open('file.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=FullLoader)

        return data


def write_data(prods):
    with open('file.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(prods, f, default_flow_style=False, allow_unicode=True)


def main():
    write_data(products)
    data = read_data()

    print(f'Data is equal: {data == products}')


if __name__ == '__main__':
    main()
