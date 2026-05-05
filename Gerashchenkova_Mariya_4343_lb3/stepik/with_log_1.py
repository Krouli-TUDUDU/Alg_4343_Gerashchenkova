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


replace_cost, insert_cost, delete_cost = map(float, input("Введите стоимости replace insert delete: ").split())

a = input("Введите строку A: ").strip()
b = input("Введите строку B: ").strip()

n = len(a)
m = len(b)

dp = [[INF] * (m + 1) for _ in range(n + 1)]

dp[0][0] = 0

for i in range(n + 1):
    for j in range(m + 1):
        if dp[i][j] == INF:
            continue

        print(f"Рассматриваем состояние dp[{i}][{j}] = {format_number(dp[i][j])}")

        if i < n and j < m:
            if a[i] == b[j]:
                new_cost = dp[i][j]

                print(f"Символы совпадают: A[{i}] = '{a[i]}' и B[{j}] = '{b[j]}'")
                print(f"Переход M: dp[{i + 1}][{j + 1}] можно обновить значением {format_number(new_cost)}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
            else:
                new_cost = dp[i][j] + replace_cost

                print(f"Символы разные: A[{i}] = '{a[i]}' и B[{j}] = '{b[j]}'")
                print(f"Переход R: заменить '{a[i]}' на '{b[j]}'")
                print(f"dp[{i + 1}][{j + 1}] можно обновить значением {format_number(new_cost)}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost

        if j < m:
            new_cost = dp[i][j] + insert_cost

            print(f"Переход I: вставить символ B[{j}] = '{b[j]}'")
            print(f"dp[{i}][{j + 1}] можно обновить значением {format_number(new_cost)}")

            if new_cost < dp[i][j + 1]:
                dp[i][j + 1] = new_cost

        if i < n:
            new_cost = dp[i][j] + delete_cost

            print(f"Переход D: удалить символ A[{i}] = '{a[i]}'")
            print(f"dp[{i + 1}][{j}] можно обновить значением {format_number(new_cost)}")

            if new_cost < dp[i + 1][j]:
                dp[i + 1][j] = new_cost

        print_matrix(dp, a, b)

print("Минимальная стоимость:")
print(format_number(dp[n][m]))