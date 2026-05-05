def print_matrix(dp, s, t):
    print("\nТекущая таблица DP:")

    print("      ", end="")
    print("  ε", end="")
    for ch in t:
        print(f"  {ch}", end="")
    print()

    for i in range(len(dp)):
        if i == 0:
            row_name = "ε"
        else:
            row_name = s[i - 1]

        print(f"{row_name:>3} ", end="")

        for value in dp[i]:
            print(f"{value:3}", end="")
        print()

    print()


s = input("Введите первую строку S: ").strip()
t = input("Введите вторую строку T: ").strip()

n = len(s)
m = len(t)

dp = [[0] * (m + 1) for _ in range(n + 1)]

for i in range(n + 1):
    dp[i][0] = i

for j in range(m + 1):
    dp[0][j] = j

print("Начальная таблица:")
print_matrix(dp, s, t)

for i in range(1, n + 1):
    for j in range(1, m + 1):
        print(f"Рассматриваем dp[{i}][{j}]")
        print(f"Сравниваем символы: S[{i - 1}] = '{s[i - 1]}' и T[{j - 1}] = '{t[j - 1]}'")

        if s[i - 1] == t[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
            print("Символы совпадают, операция не нужна")
            print(f"dp[{i}][{j}] = dp[{i - 1}][{j - 1}] = {dp[i][j]}")
        else:
            delete_cost = dp[i - 1][j] + 1
            insert_cost = dp[i][j - 1] + 1
            replace_cost = dp[i - 1][j - 1] + 1

            print("Символы разные, выбираем минимум из трёх операций:")
            print(f"Удаление: dp[{i - 1}][{j}] + 1 = {delete_cost}")
            print(f"Вставка: dp[{i}][{j - 1}] + 1 = {insert_cost}")
            print(f"Замена: dp[{i - 1}][{j - 1}] + 1 = {replace_cost}")

            dp[i][j] = min(delete_cost, insert_cost, replace_cost)

            print(f"dp[{i}][{j}] = {dp[i][j]}")

        print_matrix(dp, s, t)

print("Ответ:")
print(dp[n][m])