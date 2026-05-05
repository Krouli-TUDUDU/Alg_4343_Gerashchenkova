INF = 10 ** 18


def format_number(x):
    if abs(x - int(x)) < 1e-9:
        return str(int(x))
    return str(x)


def print_matrix(dp, a, b):
    print("\nТекущая таблица DP:")

    print("      ", end="")
    print("  ε", end="")
    for ch in b:
        print(f"  {ch}", end="")
    print()

    for i in range(len(dp)):
        if i == 0:
            row_name = "ε"
        else:
            row_name = a[i - 1]

        print(f"{row_name:>3} ", end="")

        for value in dp[i]:
            if value == INF:
                print("INF", end=" ")
            else:
                print(f"{format_number(value):>3}", end="")
        print()

    print()


def print_parent(parent):
    print("Текущая таблица операций:")

    for i in range(len(parent)):
        for j in range(len(parent[i])):
            if parent[i][j] is None:
                print(" . ", end="")
            else:
                print(f" {parent[i][j][2]} ", end="")
        print()

    print()


replace_cost, insert_cost, delete_cost = map(float, input("Введите стоимости replace insert delete: ").split())

a = input("Введите строку A: ").strip()
b = input("Введите строку B: ").strip()

n = len(a)
m = len(b)

dp = [[INF] * (m + 1) for _ in range(n + 1)]
parent = [[None] * (m + 1) for _ in range(n + 1)]

dp[0][0] = 0

for i in range(n + 1):
    for j in range(m + 1):
        if dp[i][j] == INF:
            continue

        print(f"Рассматриваем состояние dp[{i}][{j}] = {format_number(dp[i][j])}")

        if i < n and j < m:
            if a[i] == b[j]:
                new_cost = dp[i][j]

                print(f"Операция M: символы совпадают '{a[i]}' == '{b[j]}'")
                print(f"Переход: dp[{i + 1}][{j + 1}] = {format_number(new_cost)}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    parent[i + 1][j + 1] = (i, j, "M")
                    print("Обновили значение и запомнили операцию M")

            else:
                new_cost = dp[i][j] + replace_cost

                print(f"Операция R: заменить '{a[i]}' на '{b[j]}'")
                print(f"Переход: dp[{i + 1}][{j + 1}] = {format_number(new_cost)}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    parent[i + 1][j + 1] = (i, j, "R")
                    print("Обновили значение и запомнили операцию R")

        if j < m:
            new_cost = dp[i][j] + insert_cost

            print(f"Операция I: вставить символ '{b[j]}'")
            print(f"Переход: dp[{i}][{j + 1}] = {format_number(new_cost)}")

            if new_cost < dp[i][j + 1]:
                dp[i][j + 1] = new_cost
                parent[i][j + 1] = (i, j, "I")
                print("Обновили значение и запомнили операцию I")

        if i < n:
            new_cost = dp[i][j] + delete_cost

            print(f"Операция D: удалить символ '{a[i]}'")
            print(f"Переход: dp[{i + 1}][{j}] = {format_number(new_cost)}")

            if new_cost < dp[i + 1][j]:
                dp[i + 1][j] = new_cost
                parent[i + 1][j] = (i, j, "D")
                print("Обновили значение и запомнили операцию D")

        print_matrix(dp, a, b)
        print_parent(parent)

operations = []

i = n
j = m

print("Начинаем восстановление пути:")

while i > 0 or j > 0:
    prev_i, prev_j, op = parent[i][j]

    print(f"Находимся в клетке [{i}][{j}]")
    print(f"Пришли сюда из [{prev_i}][{prev_j}] операцией {op}")

    operations.append(op)

    i = prev_i
    j = prev_j

operations.reverse()

print("Минимальная стоимость:")
print(format_number(dp[n][m]))

print("Редакционное предписание:")
print("".join(operations))

print("Исходная строка A:")
print(a)

print("Исходная строка B:")
print(b)