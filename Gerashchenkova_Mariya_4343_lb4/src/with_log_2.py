def prefix_function_debug(p):
    n = len(p)
    pi = [0] * n

    print("Построение префикс-функции для шаблона:", p)
    print("Начальный массив pi:", pi)
    print()

    for i in range(1, n):
        j = pi[i - 1]

        print(f"i = {i}, p[i] = '{p[i]}', начальное j = pi[{i - 1}] = {j}")

        while j > 0 and p[i] != p[j]:
            print(f"  Несовпадение: p[{i}] = '{p[i]}' != p[{j}] = '{p[j]}'")
            print(f"  Откат: j = pi[{j - 1}] = {pi[j - 1]}")
            j = pi[j - 1]

        if p[i] == p[j]:
            print(f"  Совпадение: p[{i}] = '{p[i]}' == p[{j}] = '{p[j]}'")
            j += 1
        else:
            print(f"  Совпадения нет, j остаётся {j}")

        pi[i] = j
        print(f"  pi[{i}] = {j}")
        print("  Текущий pi:", pi)
        print()

    print("Итоговая префикс-функция:", pi)
    print()
    return pi


def cyclic_shift_debug(A, B):
    print("=== ПРОВЕРКА ЦИКЛИЧЕСКОГО СДВИГА ===")
    print("A:", A)
    print("B:", B)
    print()

    n = len(A)

    if len(A) != len(B):
        print("Длины строк разные.")
        print("Циклический сдвиг невозможен.")
        print("Ответ: -1")
        return

    if n == 0:
        print("Обе строки пустые.")
        print("Ответ: 0")
        return

    print("Строки имеют одинаковую длину.")
    print("Проверяем, входит ли B в A + A.")
    print()

    virtual_text = A + A
    print("Для понимания виртуальная строка A + A:")
    print(virtual_text)
    print()

    pi = prefix_function_debug(B)

    j = 0

    print("Начинаем искать B в виртуальной строке A + A")
    print("Но в коде символ берётся как A[i % n]")
    print()

    for i in range(2 * n - 1):
        c = A[i % n]

        print(f"i = {i}, i % n = {i % n}, текущий символ c = A[{i % n}] = '{c}', j = {j}")

        while j > 0 and c != B[j]:
            print(f"  Несовпадение: c = '{c}' != B[{j}] = '{B[j]}'")
            print(f"  Откат: j = pi[{j - 1}] = {pi[j - 1]}")
            j = pi[j - 1]

        if c == B[j]:
            print(f"  Совпадение: c = '{c}' == B[{j}] = '{B[j]}'")
            j += 1
        else:
            print(f"  Совпадения нет, j остаётся {j}")

        if j == n:
            start = i - n + 1
            print(f"  Найдено полное совпадение B!")
            print(f"  Индекс начала = i - n + 1 = {i} - {n} + 1 = {start}")

            if start < n:
                print(f"  Индекс {start} меньше n = {n}, значит он допустимый.")
                print("Ответ:", start)
                return
            else:
                print(f"  Индекс {start} не подходит, так как он не меньше n.")
                j = pi[j - 1]

        print()

    print("Строка B не найдена в A + A.")
    print("Ответ: -1")


A = input("Введите строку A: ")
B = input("Введите строку B: ")

cyclic_shift_debug(A, B)