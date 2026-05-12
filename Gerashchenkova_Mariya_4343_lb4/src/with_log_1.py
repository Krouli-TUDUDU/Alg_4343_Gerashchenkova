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


def kmp_search_debug(pattern, text):
    print("=== ПОИСК ВСЕХ ВХОЖДЕНИЙ КМП ===")
    print("Шаблон P:", pattern)
    print("Текст T:", text)
    print()

    pi = prefix_function_debug(pattern)

    result = []
    j = 0

    print("Начинаем поиск шаблона в тексте")
    print()

    for i in range(len(text)):
        print(f"i = {i}, text[i] = '{text[i]}', текущее j = {j}")

        while j > 0 and text[i] != pattern[j]:
            print(f"  Несовпадение: text[{i}] = '{text[i]}' != pattern[{j}] = '{pattern[j]}'")
            print(f"  Откат: j = pi[{j - 1}] = {pi[j - 1]}")
            j = pi[j - 1]

        if text[i] == pattern[j]:
            print(f"  Совпадение: text[{i}] = '{text[i]}' == pattern[{j}] = '{pattern[j]}'")
            j += 1
        else:
            print(f"  Совпадения нет, j остаётся {j}")

        if j == len(pattern):
            start = i - len(pattern) + 1
            print(f"  Найдено вхождение! Начальный индекс = {start}")
            result.append(start)

            print(f"  После нахождения делаем откат j = pi[{j - 1}] = {pi[j - 1]}")
            j = pi[j - 1]

        print()

    print("Результат:", result)

    if result:
        print("Ответ:", ",".join(map(str, result)))
    else:
        print("Ответ: -1")


P = input("Введите шаблон P: ")
T = input("Введите текст T: ")

kmp_search_debug(P, T)