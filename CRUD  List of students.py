"""

ЗАДАНИЕ: CRUD - операции со СПИСКОМ СТУДЕНТОВ в файле.

Программа создает/читает(поиск)/обновляет/удаляет - информацию по студентам.
Программа принимает параметр(ы): ФАМИЛИЯ и(необязательный) ИМЯ студента.

Реализована проверка ввода пользователя:
    - допустим ввод только букв русского алфавита
    - не допустим ввод пустых строк
    - не допустим ввод данных кроме Фамилии и Имени
    - при вводе можно использовать любой регист букв
    - не допустим ввод Фамилии и/или Имении по длине менее 3-х символов

Реализована защита от сбоев программы:
    - ошибки программы и системы
    - отсутствие файла для начала работы (файл создается заново)
    - ошибки при работе с файлом
"""

# import random
import os
import time
from russian_names import RussianNames  # pip install russian-names

file_stud = 'Students.txt'
RUS = 'йцукенгшщзхъфывапролджэячсмитьбюё'


def students_generator(count=10):
    """
    Генератор списка студентов: запускается из класса Students, если
    при создании объекта класса не находится файл списка студентов.
    Модуль RussianNames также устанавливается, при необходимости,
    из класса Students.
    """

    result = []
    for _ in range(count):
        a = str((RussianNames().get_person(patronymic=False))).split()
        a.reverse()
        a = ' '.join(a)
        result.append(a)
    return result


def get_students_file(function):
    """
    Создание файла списка студентов: запускается из
    класса Students, если при создании объекта класса
    не находится файл списка студентов.
    """
    students = students_generator()
    students.sort()
    list_stud = [student + '\n' for student in students]
    with open(file_stud, 'w') as f_st:
        f_st.writelines(list_stud)


class Students:
    """
    Программа создает/читает(поиск)/обновляет/удаляет -
    информацию по студентам из списка в файле.
    Программа принимает параметр(ы): ФАМИЛИЯ и(необязательный)
    ИМЯ студента.
     """

    def __init__(self, surname=None, name=None):
        self.surname = surname
        self.name = name

        self.open_file()

    def open_file(self):
        if os.path.exists(file_stud):
            try:
                with open(file_stud, 'r') as f_st:
                    info_stud = f_st.read()
                    ls = info_stud.split('\n')
                    ls.sort()
                    print()
                    print('*** НАЧАЛЬНЫЙ СПИСОК СТУДЕНТОВ *** ')
                    print(f'      файл: {file_stud}')
                    print(35 * '-')
                    for student in ls:
                        if len(student) != 0:
                            print(student)
                    print(35 * '-')
                    print()
                    time.sleep(1)
                    self.main()
            except Exception as err:
                print()
                print('ОШИБКА:', err)
                self.open_file()
        else:
            try:
                print(40 * '*')
                print(f'ФАЙЛ <{file_stud}> НЕ НАЙДЕН.')
                print('ИДЕТ СОЗДАНИЕ НОВОГО ФАЙЛА..........')
                print('ПОДОЖДИТЕ - ЭТО ЗАЙМЕТ КАКОЕ-ТО ВРЕМЯ.')
                get_students_file(students_generator())
                time.sleep(1)
                self.open_file()
            except Exception as err:
                print()
                print('ОШИБКА:', err)
                self.open_file()

    def main(self):
        print()
        print(5 * ' ' + 'МЕНЮ ВЫБОРА ДЕЙСТВИЙ:')
        print(28 * '*')
        print('1. Добавить студента\n2. Найти студента')
        print('3. Изменить данные студента\n4. Удалить студента')
        print(28 * '*')
        print()
        while True:
            choice = input \
                ('Выберите вариант из МЕНЮ (введите 1,2,3,4 или ВЫХОД <q>): ')
            menu = ('1', '2', '3', '4')
            if choice in menu:
                if choice == '1':
                    self.add_student()
                    break
                elif choice == '2':
                    self.search_student()
                    break
                elif choice == '3':
                    self.change_student_name()
                    break
                elif choice == '4':
                    self.delete_student()
                    break
            elif choice.lower() == 'q' or choice.lower() == 'й':
                print()
                print('*** ПРОГРАММА <УЧЕТА СТУДЕНТОВ> ЗАВЕРШЕНА ***')
                break
            else:
                print()
                print('!!! ОШИБКА: Некорректный ввод данных !!!')

    def add_student(self):
        try:
            print()
            while True:
                print('ВЫБРАНО МЕНЮ: ДОБАВИТЬ СТУДЕНТА.......')
                student_name = input(f'Введите через пробел ФАМИЛИЮ и ИМЯ ' +
                                     f'студента: ').split()
                if not student_name or len(student_name) == 1 or \
                        len(student_name) > 2:
                    print()
                    print('ОШИБКА:')
                    print(f'!!! У студента должна быть ФАМИЛИЯ и ИМЯ !!!')
                if len(student_name) == 2:
                    rus = 0
                    for char in (student_name[0] + student_name[1]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0] + student_name[1]) == rus:
                        if len(student_name[0]) >= 3 and \
                                len(student_name[1]) >= 3:
                            self.surname = student_name[0].capitalize()
                            self.name = student_name[1].capitalize()
                            student_name = self.surname + ' ' + self.name
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print(f'!!! Недопустимо короткая ФАМИЛИЯ' +
                                  f'и/или ИМЯ !!!')
                    else:
                        print()
                        print('ОШИБКА:')
                        print('!!! Только русский алфавит !!!')
            with open(file_stud, 'a') as f_st:
                f_st.writelines(student_name + '\n')
            print()
            print(f'*** Студент: {student_name} - добавлен в список. ***')
            with open(file_stud, 'r') as f_st:
                info_stud = f_st.read()
                ls = info_stud.split('\n')
                ls.sort()
                print()
                print('ИЗМЕНЕННЫЙ СПИСОК СТУДЕНТОВ:')
                print(f'  файл: {file_stud}')
                print(30 * '-')
                for student in ls:
                    if len(student) != 0:
                        print(student)
                print(30 * '-')
        except Exception as err:
            print()
            print('ОШИБКА:', err)
            print('!!! Повторите ввод данных заново !!!')
        finally:
            self.main()

    def search_student(self):
        try:
            print()
            while True:
                print('ВЫБРАНО МЕНЮ: НАЙТИ СТУДЕНТА.......')
                student_name = \
                    input(f'Введите через пробел ФАМИЛИЮ ' +
                          f'и(не обязательно) ИМЯ студента: ').split()
                if not student_name or len(student_name) > 2:
                    print()
                    print('ОШИБКА:')
                    print(f'!!! У студента должна быть ФАМИЛИЯ' +
                          f'(и  только ИМЯ) !!!')
                if len(student_name) == 1:
                    rus = 0
                    for char in (student_name[0]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0]) == rus:
                        if len(student_name[0]) >= 3:
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print(f'!!! Недопустимо короткая ФАМИЛИЯ ' +
                                  f'и/или ИМЯ !!!')
                    else:
                        print()
                        print('!ОШИБКА:')
                        print('!!! Только русский алфавит !!!')
                if len(student_name) == 2:
                    rus = 0
                    for char in (student_name[0] + student_name[1]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0] + student_name[1]) == rus:
                        if len(student_name[0]) >= 3 and \
                                len(student_name[1]) >= 3:
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print(f'!!! Недопустимо короткая ФАМИЛИЯ' +
                                  f'и/или ИМЯ !!!')
                    else:
                        print()
                        print('ОШИБКА:')
                        print('!!! Только русский алфавит !!!')
            if len(student_name) == 1:
                self.surname = student_name[0].capitalize()
                with open(file_stud, 'r') as f_st:
                    info_stud = f_st.read()
                    ls = info_stud.split('\n')
                    ls.sort()
                    print()
                    print('------ РЕЗУЛЬТАТ ПОИСКА СТУДЕНТОВ: ------')
                n = 0
                for student in ls:
                    if self.surname.lower() in student.lower():
                        n += 1
                        print(student)
                if n == 0:
                    print(f'Cтудент(ы) с фамилией: {self.surname} ' +
                          f'- не найден(ы).')
            if len(student_name) == 2:
                self.surname = student_name[0].capitalize()
                self.name = student_name[1].capitalize()
                student_name = self.surname + ' ' + self.name
                with open(file_stud, 'r') as f_st:
                    info_stud = f_st.read()
                    ls = info_stud.split('\n')
                    ls.sort()
                    print()
                    print('------ РЕЗУЛЬТАТ ПОИСКА СТУДЕНТОВ: ------')
                    n = 0
                    for student in ls:
                        if student_name.lower() == student.lower():
                            n += 1
                            print(f'Студент: {student_name} -  ' +
                                  f'есть в списке.')
                    if n == 0:
                        print(f'Cтудента: {student_name} - НЕТ в списке.')
        except Exception as err:
            print()
            print('ОШИБКА:', err)
            print('!!! Повторите ввод данных заново !!!')
        finally:
            self.main()

    def change_student_name(self):
        try:
            while True:
                print()
                print('ВЫБРАНО МЕНЮ: ИЗМЕНИТЬ ДАННЫЕ СТУДЕНТА......')
                student_name = input(f'Введите через пробел ФАМИЛИЮ и ' +
                                     f'ИМЯ студента: ').split()
                if not student_name or len(student_name) == 1 or \
                        len(student_name) > 2:
                    print()
                    print('ОШИБКА:')
                    print(f'!!! У студента должна быть ФАМИЛИЯ и ИМЯ !!!')
                if len(student_name) == 2:
                    rus = 0
                    for char in (student_name[0] + student_name[1]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0] + student_name[1]) == rus:
                        if len(student_name[0]) >= 3 and \
                                len(student_name[1]) >= 3:
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print(f'!!! Недопустимо короткая ФАМИЛИЯ ' +
                                  f'и/или ИМЯ !!!')
                    else:
                        print()
                        print('ОШИБКА:')
                        print('!!! Только русский алфавит !!!')

            self.surname = student_name[0].capitalize()
            self.name = student_name[1].capitalize()
            student_name = self.surname + ' ' + self.name
            with open(file_stud, 'r') as f_st:
                info_stud = f_st.read()
                ls = info_stud.split('\n')
                ls.sort()
                print()
                print('------ РЕЗУЛЬТАТ ПОИСКА СТУДЕНТОВ: ------')
                n = 0
                for student in ls:
                    if student_name.lower() == student.lower():
                        n += 1
                        print(f'Студент: {student_name} - есть в списке.')
                        while True:
                            new_student_surname = \
                                input(f'Введите НОВУЮ ФАМИЛИЮ ' +
                                      f'студента, если не меняется - Enter: ').split()
                            if not new_student_surname or \
                                    len(new_student_surname) > 2:
                                print()
                                print('ОШИБКА:')
                                print(f'!!! У студента должна быть только ' +
                                      f'ФАМИЛИЯ!!!')
                            if len(new_student_surname) == 1:
                                rus = 0
                                for char in (new_student_surname[0]):
                                    if char.lower() in RUS:
                                        rus += 1
                                if len(new_student_surname[0]) == rus:
                                    if len(new_student_surname[0]) >= 3:
                                        break
                                    else:
                                        print()
                                        print('ОШИБКА:')
                                        print('!!! Недопустимо короткая ' +
                                              f'ФАМИЛИЯ !!!')
                                else:
                                    print()
                                    print('!!! ОШИБКА:')
                                    print('!!! Только русский алфавит !!!')

                        while True:
                            new_student_name = input \
                                (f'Введите НОВОЕ ИМЯ студента, если не' +
                                 f'меняется - Enter: ').split()
                            if not new_student_name or \
                                    len(new_student_name) > 2:
                                print()
                                print('ОШИБКА:')
                                print(f'!!! У студента должно быть ' +
                                      f'только ИМЯ !!!')
                            if len(new_student_name) == 1:
                                rus = 0
                                for char in (new_student_name[0]):
                                    if char.lower() in RUS:
                                        rus += 1
                                if len(new_student_name[0]) == rus:
                                    if len(new_student_name[0]) >= 3:
                                        break
                                    else:
                                        print()
                                        print('ОШИБКА:')
                                        print(f'!!! Недопустимо ' +
                                              f'короткое ИМЯ !!!')
                                else:
                                    print()
                                    print('ОШИБКА:')
                                    print('!!! Только русский алфавит !!!')

                        if len(new_student_surname) != 0 and \
                                len(new_student_name) != 0:
                            self.surname = new_student_surname[0].capitalize()
                            self.name = new_student_name[0].capitalize()
                            new_student = self.surname + ' ' + self.name
                            print()
                            print(f'*** Замена: {student_name} - на: ' +
                                  f'{new_student} ***')
                            f_st.close()
                            with open(file_stud, 'a') as f_st:
                                f_st.writelines(new_student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                ls.remove(student_name)
                            with open(file_stud, 'w') as f_st:
                                for student in ls:
                                    f_st.writelines(student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                print()
                                print('РЕЗУЛЬТАТ ИЗМЕНЕНИЯ СПИСКА СТУДЕНТОВ:')
                                print(f'      файл: {file_stud}')
                                print(30 * '-')
                                for student in ls:
                                    if len(student) != 0:
                                        print(student)
                                print(30 * '-')
                        elif len(new_student_surname) != 0 and \
                                len(new_student_name) == 0:
                            self.surname = new_student_surname[0].capitalize()
                            new_student = \
                                str(self.surname) + ' ' + str(self.name)
                            print()
                            print(f'*** Замена: {student_name}> - на: ' +
                                  f'{new_student} ***')
                            f_st.close()
                            with open(file_stud, 'a') as f_st:
                                f_st.writelines(new_student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                ls.remove(student_name)
                            with open(file_stud, 'w') as f_st:
                                for student in ls:
                                    f_st.writelines(student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                print()
                                print('РЕЗУЛЬТАТ ИЗМЕНЕНИЯ СПИСКА СТУДЕНТОВ:')
                                print(f'      файл: {file_stud}')
                                print(30 * '-')
                                for student in ls:
                                    if len(student) != 0:
                                        print(student)
                                print(30 * '-')
                        elif len(new_student_surname) == 0 and \
                                len(new_student_name) != 0:
                            self.name = new_student_name
                            new_student = \
                                str(self.surname) + ' ' + str(self.name)
                            print()
                            print(f'*** Замена: {student_name} - на: ' +
                                  f'{new_student} ***')
                            f_st.close()
                            with open(file_stud, 'a') as f_st:
                                f_st.writelines(new_student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                ls.remove(student_name)
                            with open(file_stud, 'w') as f_st:
                                for student in ls:
                                    f_st.writelines(student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                print()
                                print('РЕЗУЛЬТАТ ИЗМЕНЕНИЯ СПИСКА СТУДЕНТОВ:')
                                print(f'      файл: {file_stud}')
                                print(30 * '-')
                                for student in ls:
                                    if len(student) != 0:
                                        print(student)
                                print(30 * '-')
                if n == 0:
                    print(f'Cтудента: {student_name} - НЕТ в списке.')
        except Exception as err:
            print()
            print('ОШИБКА:', err)
            print('!!! Повторите ввод данных заново !!!')
        finally:
            self.main()

    def delete_student(self):
        try:
            print()
            while True:
                print('ВЫБРАНО МЕНЮ: УДАЛИТЬ СТУДЕНТА......')
                student_name = input \
                    (f'Введите ФАМИЛИЮ и(не обязательно) ИМЯ ' +
                     f'студента: ').split()
                if not student_name or len(student_name) > 2:
                    print()
                    print('ОШИБКА:')
                    print(f'!!! У студента должна быть ' +
                          f'ФАМИЛИЯ (и ИМЯ) !!!')
                if len(student_name) == 1:
                    rus = 0
                    for char in (student_name[0]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0]) == rus:
                        if len(student_name[0]) >= 3:
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print('!!! Недопустимо короткая ФАМИЛИЯ !!!')
                    else:
                        print()
                        print('ОШИБКА:')
                        print('!!! Только русский алфавит !!!')
                if len(student_name) == 2:
                    rus = 0
                    for char in (student_name[0] + student_name[1]):
                        if char.lower() in RUS:
                            rus += 1
                    if len(student_name[0] + student_name[1]) == rus:
                        if len(student_name[0]) >= 3 and \
                                len(student_name[1]) >= 3:
                            break
                        else:
                            print()
                            print('ОШИБКА:')
                            print(f'!!! Недопустимо короткая ФАМИЛИЯ ' +
                                  f'и/или ИМЯ !!!')
                    else:
                        print()
                        print('ОШИБКА:')
                        print('Только русский алфавит !!!')

            if len(student_name) == 2:
                self.surname = student_name[0].capitalize()
                self.name = student_name[1].capitalize()
                student_name = self.surname + ' ' + self.name
                with open(file_stud, 'r') as f_st:
                    info_stud = f_st.read()
                    ls = info_stud.split('\n')
                    ls.sort()
                    n = 0
                    for student in ls:
                        if student_name.lower() == student.lower():
                            n += 1
                            print()
                            print(f'*** Студент: {student_name} ' +
                                  f'- удален из списка. ***')
                            f_st.close()
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                ls.remove(student_name)
                            with open(file_stud, 'w') as f_st:
                                for student in ls:
                                    f_st.writelines(student + '\n')
                            with open(file_stud, 'r') as f_st:
                                info_stud = f_st.read()
                                ls = info_stud.split('\n')
                                ls.sort()
                                print()
                                print(f'РЕЗУЛЬТАТ ПОСЛЕ УДАЛЕНИЯ ' +
                                      f'СТУДЕНТА ИЗ СПИСКА:')
                                print(f'          файл: {file_stud}')
                                print(30 * '-')
                                for student in ls:
                                    if len(student) != 0:
                                        print(student)
                                print(30 * '-')
                    if n == 0:
                        print()
                        print(f'*** Cтудента: {student_name} - ' +
                              f'НЕТ в списке. ***')
            elif len(student_name) == 1:
                self.surname = student_name[0].capitalize()
                with open(file_stud, 'r') as f_st:
                    info_stud = f_st.read()
                    ls = info_stud.split('\n')
                    ls.sort()
                    n = 0
                    ls_student = []
                    for student in ls:
                        if self.surname.lower() in student.lower():
                            n += 1
                            ls_student.append(student)
                            print(student)
                    if n == 0:
                        print()
                        print(f'*** Cтудента: {self.surname} - ' +
                              f'НЕТ в списке. ***')
                    if n == 1:
                        print()
                        print(f'*** Студент <{ls_student[0]}> ' +
                              f'- удален из списка. ***')
                        f_st.close()
                        with open(file_stud, 'r') as f_st:
                            info_stud = f_st.read()
                            ls = info_stud.split('\n')
                            ls.sort()
                            ls.remove(ls_student[0])
                        with open(file_stud, 'w') as f_st:
                            for student in ls:
                                f_st.writelines(student + '\n')
                        with open(file_stud, 'r') as f_st:
                            info_stud = f_st.read()
                            ls = info_stud.split('\n')
                            ls.sort()
                            print()
                            print(f'РЕЗУЛЬТАТ ПОСЛЕ УДАЛЕНИЯ СТУДЕНТА ' +
                                  f'ИЗ СПИСКА:')
                            print(f'         файл: {file_stud}')
                            print(30 * '-')
                            for student in ls:
                                if len(student) != 0:
                                    print(student)
                            print(30 * '-')
                    if n > 1:
                        while True:
                            student_name_d = \
                                input('Введите ИМЯ студента: ').split()
                            if not student_name_d or \
                                    len(student_name_d) > 1:
                                print()
                                print('ОШИБКА:')
                                print(f'!!! У студента должно быть ' +
                                      f'только Имя !!!')

                            if len(student_name_d) == 1:
                                rus = 0
                                for char in (student_name_d[0]):
                                    if char.lower() in RUS:
                                        rus += 1
                                if len(student_name_d[0]) == rus:
                                    if len(student_name_d[0]) >= 3:
                                        break
                                    else:
                                        print()
                                        print('ОШИБКА:')
                                        print(f'!!! Недопустимо ' +
                                              f'короткое ИМЯ !!!')
                                else:
                                    print()
                                    print('ОШИБКА:')
                                    print('!!! Только русский алфавит !!!')

                        self.name = student_name_d[0].capitalize()
                        student_name = self.surname + ' ' + self.name
                        print()
                        print(f'*** Студент: {student_name} ' +
                              f'- удален из списка. ***')
                        f_st.close()
                        with open(file_stud, 'r') as f_st:
                            info_stud = f_st.read()
                            ls = info_stud.split('\n')
                            ls.sort()
                            ls.remove(student_name)
                        with open(file_stud, 'w') as f_st:
                            for student in ls:
                                f_st.writelines(student + '\n')
                        with open(file_stud, 'r') as f_st:
                            info_stud = f_st.read()
                            ls = info_stud.split('\n')
                            ls.sort()
                            print()
                            print(f'РЕЗУЛЬТАТ ПОСЛЕ УДАЛЕНИЯ СТУДЕНТА ' +
                                  f'ИЗ СПИСКА:')
                            print(f'         файл: {file_stud}')
                            print(30 * '-')
                            for student in ls:
                                if len(student) != 0:
                                    print(student)
                            print(30 * '-')
        except Exception as err:
            print()
            print('ОШИБКА:', err)
            print('!!! Повторите ввод данных заново !!!')
        finally:
            self.main()


student = Students()
