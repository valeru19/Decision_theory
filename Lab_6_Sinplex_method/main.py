M = 1e4  # Большое число для искусственного добавления ограничений в таблицу

# Начальная таблица симплекс-метода
simplex_table = [
    [-20*M, -3*M-3, -4*M+2, 0, 0, M, 0],  # Строки с коэффициентами целевой функции и переменными
    [11, 2, 1, 1, 0, 0, 0],  # Ограничения задачи
    [10, -3, 2, 0, 1, 0, 0],
    [20, 3, 4, 0, 0, -1, 1]
]

# Начальное решение
solution = [0, 0, 0, 0, 0, 0]
indexes = []  # Список индексов ведущих строк и столбцов

# Функция для поиска ведущего столбца
def find_leading_column(matrix):
    temp_matrix = matrix[0].copy()  # Копируем первую строку
    temp_matrix.pop(0)  # Удаляем первый элемент (это значение целевой функции)
    lead_column = temp_matrix.index(min(temp_matrix))  # Находим индекс минимального элемента в строке
    return lead_column + 1  # Возвращаем индекс столбца, добавляя 1 для соответствия индексации в таблице

# Функция для поиска ведущей строки
def find_leading_row(matrix):
    lead_column = find_leading_column(matrix)  # Находим ведущий столбец
    quotients = []  # Список для хранения значений отношения правой части к элементам ведущего столбца
    for i in range(1, len(matrix)):  # Проходим по строкам (начиная с 1, так как 0 — это строка целевой функции)
        if matrix[i][lead_column] > 0:  # Если элемент в ведущем столбце положительный
            quotients.append(matrix[i][0] / matrix[i][lead_column])  # Вычисляем отношение
        else:
            quotients.append(1e8)  # Если элемент в ведущем столбце меньше или равен 0, добавляем большое число
    lead_row = quotients.index(min(quotients))  # Находим строку с минимальным отношением
    return lead_row + 1  # Возвращаем индекс ведущей строки (с учетом индексации)

# Функция для обновления симплекс-таблицы
def write_new_table(matrix):
    lead_row = find_leading_row(matrix)  # Находим ведущую строку
    lead_column = find_leading_column(matrix)  # Находим ведущий столбец
    new_matrix = []  # Новая таблица
    matrix_row = []  # Вспомогательная переменная для строк новой таблицы
    lead_element = matrix[lead_row][lead_column]  # Ведущий элемент
    for i in range(len(matrix)):  # Проходим по всем строкам таблицы
        if i != lead_row:  # Если текущая строка не ведущая
            for j in range(len(matrix[0])):  # Проходим по всем столбцам
                if j != lead_column:  # Если текущий столбец не ведущий
                    matrix_row.append(
                        matrix[i][j] - (matrix[i][lead_column] * matrix[lead_row][j]) / lead_element  # Обновляем элементы
                    )
                else:
                    matrix_row.append(0)  # В ведущем столбце обнуляем элементы
        else:
            for j in range(len(matrix[0])):  # Для ведущей строки
                matrix_row.append(matrix[i][j] / lead_element)  # Обновляем элементы ведущей строки
        new_matrix.append(matrix_row.copy())  # Добавляем обновленную строку в новую таблицу
        matrix_row.clear()  # Очищаем список для следующей строки
    return new_matrix  # Возвращаем новую таблицу

# Функция для проверки, завершено ли решение симплекс-метода
def simplex_done(matrix):
    for i in range(len(matrix[0])):  # Проходим по всем элементам первой строки
        if matrix[0][i] < 0:  # Если хотя бы один элемент отрицателен
            return False  # Решение не завершено
    return True  # Все элементы первой строки неотрицательные — решение завершено

# Функция для проверки, нет ли решений у задачи
def simplex_unsolving(matrix):
    for i in range(len(matrix)):  # Проходим по всем строкам таблицы
        for j in range(len(matrix[i])):  # Проходим по всем столбцам
            if matrix[i][j] > 0:  # Если хотя бы один элемент положителен
                return False  # Решений нет
    return True  # Если все элементы не положительные — решение существует

# Основной цикл симплекс-метода
while not(simplex_done(simplex_table)):  # Пока не найдено оптимальное решение
    if simplex_unsolving(simplex_table):  # Если решение невозможно
        print('Решений у задачи нет.')
        break
    print("\nТекущая таблица симплекс-метода:")
    print("+" + "-" * 60 + "+")  # Печать верхней границы таблицы
    # Печать таблицы в формате симплекс-таблицы
    print("| {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} |".format(
        "Z", "x1", "x2", "s1", "s2", "a1", "a2"))  # Заголовки столбцов
    print("+" + "-" * 60 + "+")
    for row in simplex_table:  # Печатаем все строки таблицы
        print("|", end="")
        for cell in row:
            print(f" {round(cell, 4):<10} |", end="")  # Округляем значения и выравниваем по левому краю
        print("\n+" + "-" * 60 + "+")  # Печатаем нижнюю границу каждой строки

    indexes.append((find_leading_row(simplex_table), find_leading_column(simplex_table)))  # Добавляем индексы ведущих строк и столбцов
    simplex_table = write_new_table(simplex_table)  # Обновляем таблицу

# Выводим итоговую таблицу
print("\nФинальная таблица симплекс-метода:")
print("+" + "-" * 60 + "+")  # Печать верхней границы таблицы
# Печать финальной таблицы
print("| {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} |".format(
    "Z", "x1", "x2", "s1", "s2", "a1", "a2"))  # Заголовки столбцов
print("+" + "-" * 60 + "+")
for row in simplex_table:  # Печатаем все строки финальной таблицы
    print("|", end="")
    for cell in row:
        print(f" {round(cell, 4):<10} |", end="")  # Округляем значения и выравниваем по левому краю
    print("\n+" + "-" * 60 + "+")

# Находим решение
for cortez in indexes:
    solution[cortez[1] - 1] = simplex_table[cortez[0]][0]  # Записываем решения в список

# Формализованный вывод результатов
print("\nРешение задачи:")
for i in range(len(solution)):  # Выводим значения переменных
    print(f"Переменная x{i + 1}: {round(solution[i], 2)}")
print(f"\nЗначение целевой функции: f = {round(simplex_table[0][0], 2)}")
