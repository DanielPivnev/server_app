"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']

for i in range(len(words)):
    words[i] = words[i].encode(encoding='utf-8')
    print('————————————————————————————')
    print('Слова:', words[i], '\nТип:', type(words[i]))

for i in range(len(words)):
    words[i] = words[i].decode(encoding='utf-8')
    print('————————————————————————————')
    print('Слова:', words[i], '\nТип:', type(words[i]))
