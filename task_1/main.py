"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import os
import pathlib
import re


def get_data():
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    for file in os.listdir(pathlib.Path(__file__).parent.resolve()):
        if file.endswith('txt'):
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line in lines:
                    if 'Изготовитель системы' in line:
                        data = line.split(':')[1].replace(' ', '').replace('\n', '')
                        os_prod_list.append(data)
                    elif 'Название ОС' in line:
                        mapped_data = re.search(r'Windows[0-9.]*.?[0-9.]*', line)
                        os_name_list.append(line[mapped_data.start():mapped_data.end()])
                    elif 'Код продукта' in line:
                        data = line.split(':')[1].replace(' ', '').replace('\n', '')
                        os_code_list.append(data)
                    elif 'Тип системы' in line:
                        data = line.split(':')[1].replace(' ', '').replace('\n', '')
                        os_type_list.append(data)

    return [headers, os_prod_list, os_name_list, os_code_list, os_type_list]


def write_data(data):
    with open('data_report.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow(data[0])
        for i in range(1, len(data) - 1):
            writer.writerow([i] + [data[1][i - 1]] + [data[2][i - 1]] + [data[3][i - 1]] + [data[4][i - 1]])
            writer.writerow([])


def main():
    data = get_data()
    write_data(data)


if __name__ == '__main__':
    main()
