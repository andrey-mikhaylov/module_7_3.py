import os
import sys
import re


class WordsFinder:
    def __init__(self, *file_names: str):
        """
        записывает названия файлов в атрибут file_names в виде списка.
        :param filenames: неограниченное количество названий файлов
        """
        self.file_names = file_names

    def __read_file(self, file_name: str) -> str:
        with open(file_name, 'r', encoding='utf8') as f:
            text = f.read()
        return text

    def __remove_symbols(self, text: str, symbols: list[str], new: str) -> str:
        for symbol in symbols:
            text = text.replace(symbol, new)
        return text

    def get_all_words(self):
        """
        подготовительный метод, который возвращает словарь названий файлов и слов, содержащиеся в этих файлах
        :return: словарь следующего вида:
                 {'file1.txt': ['word1', 'word2'], 'file2.txt': ['word3', 'word4'], 'file3.txt': ['word5', 'word6', 'word7']}
        """
        # Создайте пустой словарь all_words.
        all_words = {}

        # Переберите названия файлов и открывайте каждый из них, используя оператор with.
        for file_name in self.file_names:
            # Для каждого файла считывайте единые строки, переводя их в нижний регистр (метод lower()).
            text = self.__read_file(file_name).lower()
            # Избавьтесь от пунктуации [',', '.', '=', '!', '?', ';', ':', ' - '] в строке. (тире обособлено пробелами, это не дефис в слове).
            text1 = self.__remove_symbols(text, ['!', ' - '], '')
            text2 = self.__remove_symbols(text1, [',', '.', '=', '?', ';', ':'], ' ')     #'—',  '‘', '’' ???
            # Разбейте эту строку на элементы списка методом split(). (разбивается по умолчанию по пробелу)
            words = text2.split()
            # В словарь all_words запишите полученные данные, ключ - название файла, значение - список из слов этого файла.
            all_words[file_name] = words

        return all_words

    def find(self, word: str) -> dict[str, int]:
        """
        :param word: искомое слово
        :return: словарь, где ключ - название файла, значение - позиция первого такого слова в списке слов этого файла.
        """
        # В методах find и count пользуйтесь ранее написанным методом get_all_words для получения названия файла и списка его слов.
        # Для удобного перебора одновременно ключа(названия) и значения(списка слов) можно воспользоваться методом словаря - item().
        result = {}
        for file_name, words in self.get_all_words().items():
            # Логика методов find или count
            position = words.index(word.lower()) + 1
            result[file_name] = position

        return result

    def count(self, word: str) -> dict[str, int]:
        """
        :param word: искомое слово
        :return: словарь, где ключ - название файла, значение - количество слова word в списке слов этого файла.
        """
        result = {}
        for file_name, words in self.get_all_words().items():
            # Логика методов find или count
            #position = words.index(word.lower())
            result[file_name] = words.count(word.lower())

        return result


def test1():
    finder2 = WordsFinder('test_file.txt')
    print(finder2.get_all_words())  # Все слова
    print(finder2.find('TEXT'))  # 3 слово по счёту
    print(finder2.count('teXT'))  # 4 слова teXT в тексте всего
    """
    Вывод на консоль:
    {'test_file.txt': ["it's", 'a', 'text', 'for', 'task', 'найти', 'везде', 'используйте', 'его', 'для', 'самопроверки', 'успехов', 'в', 'решении', 'задачи', 'text', 'text', 'text']}
    {'test_file.txt': 3}
    {'test_file.txt': 4}
    """


def test2():
    finder1 = WordsFinder('Mother Goose - Monday’s Child.txt',)
    print(finder1.get_all_words())
    print(finder1.find('Child'))
    print(finder1.count('Child'))


def test3():
    finder1 = WordsFinder('Rudyard Kipling - If.txt', )
    print(finder1.get_all_words())
    print(finder1.find('if'))
    print(finder1.count('if'))


def test4():
    finder1 = WordsFinder('Walt Whitman - O Captain! My Captain!.txt')
    print(finder1.get_all_words())
    print(finder1.find('captain'))
    print(finder1.count('captain'))

def test5():
    finder1 = WordsFinder('Walt Whitman - O Captain! My Captain!.txt',
                          'Rudyard Kipling - If.txt',
                          'Mother Goose - Monday’s Child.txt')
    print(finder1.get_all_words())
    print(finder1.find('the'))
    print(finder1.count('the'))


def run_test(test_dir: str, test_fn):
    main_dir = os.getcwd()
    if (test_dir):
        os.chdir(test_dir)

    class ListStream:
        def __init__(self):
            self.data = ''

        def write(self, s):
            self.data += s

        def flush(self):
            pass

    sys.stdout = x = ListStream()
    test_fn()
    result = x.data
    sys.stdout = sys.__stdout__

    with open('result.txt', 'r', encoding='utf8') as f:
        correct_result = f.read()

    with open('my_result.txt', 'w', encoding='utf8') as f:
        f.write(result)

    if result == correct_result:
        print(result)
    else:
        print(f"fail\ngot:\n{x.data}correct:\n{correct_result}")
        raise

    os.chdir(main_dir)


if __name__ == '__main__':
#    test1()
     run_test('', test1)
     run_test('Mother Goose - Monday’s Child', test2)
     run_test('Rudyard Kipling - If', test3)
     run_test('Walt Whitman - O Captain! My Captain!', test4)
     run_test('All', test5)


"""
2023/11/17 00:00|Домашнее задание по теме "Оператор "with".
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.

Цель: применить на практике оператор with, вспомнить написание кода в парадигме ООП.

Задача "Найдёт везде":
Напишите класс WordsFinder, объекты которого создаются следующим образом:
WordsFinder('file1.txt, file2.txt', 'file3.txt', ...).
Объект этого класса должен принимать при создании неограниченного количество названий файлов и записывать их в атрибут file_names в виде списка или кортежа.

Также объект класса WordsFinder должен обладать следующими методами:
get_all_words - подготовительный метод, который возвращает словарь следующего вида:
{'file1.txt': ['word1', 'word2'], 'file2.txt': ['word3', 'word4'], 'file3.txt': ['word5', 'word6', 'word7']}
Где:
'file1.txt', 'file2.txt', ''file3.txt'' - названия файлов.
['word1', 'word2'], ['word3', 'word4'], ['word5', 'word6', 'word7'] - слова содержащиеся в этом файле.
Алгоритм получения словаря такого вида в методе get_all_words:
Создайте пустой словарь all_words.
Переберите названия файлов и открывайте каждый из них, используя оператор with.
Для каждого файла считывайте единые строки, переводя их в нижний регистр (метод lower()).
Избавьтесь от пунктуации [',', '.', '=', '!', '?', ';', ':', ' - '] в строке. (тире обособлено пробелами, это не дефис в слове).
Разбейте эту строку на элементы списка методом split(). (разбивается по умолчанию по пробелу)
В словарь all_words запишите полученные данные, ключ - название файла, значение - список из слов этого файла.

find(self, word) - метод, где word - искомое слово. Возвращает словарь, где ключ - название файла, значение - позиция первого такого слова в списке слов этого файла.
count(self, word) - метод, где word - искомое слово. Возвращает словарь, где ключ - название файла, значение - количество слова word в списке слов этого файла.
В методах find и count пользуйтесь ранее написанным методом get_all_words для получения названия файла и списка его слов.
Для удобного перебора одновременно ключа(названия) и значения(списка слов) можно воспользоваться методом словаря - item().

for name, words in get_all_words().items():
  # Логика методов find или count

Пример результата выполнения программы:
Представим, что файл 'test_file.txt' содержит следующий текст:


Пример выполнения программы:
finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words()) # Все слова
print(finder2.find('TEXT')) # 3 слово по счёту
print(finder2.count('teXT')) # 4 слова teXT в тексте всего

Вывод на консоль:
{'test_file.txt': ["it's", 'a', 'text', 'for', 'task', 'найти', 'везде', 'используйте', 'его', 'для', 'самопроверки', 'успехов', 'в', 'решении', 'задачи', 'text', 'text', 'text']}
{'test_file.txt': 3}
{'test_file.txt': 4}

Запустите этот код с другими примерами предложенными здесь.
Если решение верное, то результаты должны совпадать с предложенными.

Примечания:
Регистром слов при поиске можно пренебречь. ('teXT' ~ 'text')
Решайте задачу последовательно - написав один метод, проверьте результаты его работы.

Файл module_7_3.py и загрузите его на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""
