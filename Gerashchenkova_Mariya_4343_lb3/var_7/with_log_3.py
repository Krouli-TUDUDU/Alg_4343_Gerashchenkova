INF = 10 ** 9


def can_replace(s, index, cursed, variant):
    if index not in cursed:
        return True

    if variant == "7b" and s[index].lower() == "z":
        return True

    return False


def can_delete(s, index, cursed, variant):
    if index not in cursed:
        return True

    if variant == "7a" and s[index].lower() == "u":
        return True

    return False


def print_dp(dp, a, b):
    print("\nТекущая таблица dp:")

    print("      ε", end="")
    for ch in b:
        print(f"{ch:>5}", end="")
    print()

    for i in range(len(dp)):
        if i == 0:
            row_name = "ε"
        else:
            row_name = a[i - 1]

        print(f"{row_name:>3}", end="")

        for value in dp[i]:
            if value == INF:
                print(f"{'∞':>5}", end="")
            else:
                print(f"{value:>5}", end="")
        print()

    print()


def main():
    a = input().strip()
    b = input().strip()

    variant = input().strip()

    k = int(input())

    if k > 0:
        cursed_indices = list(map(int, input().split()))
    else:
        cursed_indices = []

    cursed = set(index - 1 for index in cursed_indices)

    n = len(a)
    m = len(b)

    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    print("Исходные данные:")
    print("A =", a)
    print("B =", b)
    print("Подвариант =", variant)
    print("Проклятые индексы =", cursed_indices)

    if cursed_indices:
        print("Проклятые символы:")
        for index in cursed_indices:
            print(f"индекс {index}: символ '{a[index - 1]}'")

    print_dp(dp, a, b)

    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue

            print("=" * 60)
            print(f"Рассматриваем клетку dp[{i}][{j}] = {dp[i][j]}")

            if i < n and j < m and a[i] == b[j]:
                new_cost = dp[i][j]

                print("\nОперация M — совпадение")
                print(f"A[{i}] = '{a[i]}', B[{j}] = '{b[j]}'")
                print("Символы совпадают, стоимость не увеличивается.")
                print(f"Переход в dp[{i + 1}][{j + 1}] со стоимостью {new_cost}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    print("Клетка обновлена.")
                else:
                    print("Клетка не обновлена, потому что текущее значение лучше.")

            if i < n and j < m and a[i] != b[j]:
                print("\nОперация R — замена")
                print(f"Нужно заменить A[{i}] = '{a[i]}' на B[{j}] = '{b[j]}'.")

                if can_replace(a, i, cursed, variant):
                    new_cost = dp[i][j] + 1

                    print("Замена разрешена.")
                    print(f"Стоимость: {dp[i][j]} + 1 = {new_cost}")
                    print(f"Переход в dp[{i + 1}][{j + 1}]")

                    if new_cost < dp[i + 1][j + 1]:
                        dp[i + 1][j + 1] = new_cost
                        print("Клетка обновлена.")
                    else:
                        print("Клетка не обновлена, потому что текущее значение лучше.")
                else:
                    print("Замена запрещена из-за проклятого символа.")

            if j < m:
                new_cost = dp[i][j] + 1

                print("\nОперация I — вставка")
                print(f"Вставляем символ B[{j}] = '{b[j]}'.")
                print("Вставка всегда разрешена.")
                print(f"Стоимость: {dp[i][j]} + 1 = {new_cost}")
                print(f"Переход в dp[{i}][{j + 1}]")

                if new_cost < dp[i][j + 1]:
                    dp[i][j + 1] = new_cost
                    print("Клетка обновлена.")
                else:
                    print("Клетка не обновлена, потому что текущее значение лучше.")

            if i < n:
                print("\nОперация D — удаление")
                print(f"Нужно удалить A[{i}] = '{a[i]}'.")

                if can_delete(a, i, cursed, variant):
                    new_cost = dp[i][j] + 1

                    print("Удаление разрешено.")
                    print(f"Стоимость: {dp[i][j]} + 1 = {new_cost}")
                    print(f"Переход в dp[{i + 1}][{j}]")

                    if new_cost < dp[i + 1][j]:
                        dp[i + 1][j] = new_cost
                        print("Клетка обновлена.")
                    else:
                        print("Клетка не обновлена, потому что текущее значение лучше.")
                else:
                    print("Удаление запрещено из-за проклятого символа.")

            print_dp(dp, a, b)

    print("=" * 60)
    print("Итог:")

    if dp[n][m] == INF:
        print("Преобразование невозможно.")
        print("Impossible")
    else:
        print("Минимальное расстояние Левенштейна:")
        print(dp[n][m])


main()