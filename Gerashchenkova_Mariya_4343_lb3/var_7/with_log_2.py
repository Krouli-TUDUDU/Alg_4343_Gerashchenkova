INF = 10 ** 18


def format_number(x):
    if abs(x - int(x)) < 1e-9:
        return str(int(x))
    return str(x)


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
        print(f"{ch:>6}", end="")
    print()

    for i in range(len(dp)):
        if i == 0:
            row_name = "ε"
        else:
            row_name = a[i - 1]

        print(f"{row_name:>3}", end="")

        for value in dp[i]:
            if value == INF:
                print(f"{'∞':>6}", end="")
            else:
                print(f"{format_number(value):>6}", end="")
        print()

    print()


def main():
    replace_cost, insert_cost, delete_cost = map(float, input().split())

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
    print("Стоимость replace =", format_number(replace_cost))
    print("Стоимость insert =", format_number(insert_cost))
    print("Стоимость delete =", format_number(delete_cost))
    print("Подвариант =", variant)
    print("Проклятые индексы =", cursed_indices)

    if cursed_indices:
        print("Проклятые символы:")
        for index in cursed_indices:
            print(f"индекс {index}: символ '{a[index - 1]}'")

    print("\nПравило треугольника:")
    print("replace_cost <= delete_cost + insert_cost")
    print(
        f"{format_number(replace_cost)} <= "
        f"{format_number(delete_cost)} + {format_number(insert_cost)}"
    )

    if replace_cost <= delete_cost + insert_cost:
        print("Правило треугольника выполняется.")
    else:
        print("Правило треугольника не выполняется.")

    print_dp(dp, a, b)

    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue

            print("=" * 60)
            print(f"Рассматриваем клетку dp[{i}][{j}] = {format_number(dp[i][j])}")

            if i < n and j < m and a[i] == b[j]:
                new_cost = dp[i][j]

                print("\nОперация M — совпадение")
                print(f"A[{i}] = '{a[i]}', B[{j}] = '{b[j]}'")
                print("Символы совпадают, стоимость не увеличивается.")
                print(f"Переход в dp[{i + 1}][{j + 1}] со стоимостью {format_number(new_cost)}")

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    print("Клетка обновлена.")
                else:
                    print("Клетка не обновлена.")

            if i < n and j < m and a[i] != b[j]:
                print("\nОперация R — замена")
                print(f"Нужно заменить A[{i}] = '{a[i]}' на B[{j}] = '{b[j]}'.")

                if can_replace(a, i, cursed, variant):
                    new_cost = dp[i][j] + replace_cost

                    print("Замена разрешена.")
                    print(
                        f"Стоимость: {format_number(dp[i][j])} + "
                        f"{format_number(replace_cost)} = {format_number(new_cost)}"
                    )
                    print(f"Переход в dp[{i + 1}][{j + 1}]")

                    if new_cost < dp[i + 1][j + 1]:
                        dp[i + 1][j + 1] = new_cost
                        print("Клетка обновлена.")
                    else:
                        print("Клетка не обновлена.")
                else:
                    print("Замена запрещена из-за проклятого символа.")

            if j < m:
                new_cost = dp[i][j] + insert_cost

                print("\nОперация I — вставка")
                print(f"Вставляем символ B[{j}] = '{b[j]}'.")
                print("Вставка всегда разрешена.")
                print(
                    f"Стоимость: {format_number(dp[i][j])} + "
                    f"{format_number(insert_cost)} = {format_number(new_cost)}"
                )
                print(f"Переход в dp[{i}][{j + 1}]")

                if new_cost < dp[i][j + 1]:
                    dp[i][j + 1] = new_cost
                    print("Клетка обновлена.")
                else:
                    print("Клетка не обновлена.")

            if i < n:
                print("\nОперация D — удаление")
                print(f"Нужно удалить A[{i}] = '{a[i]}'.")

                if can_delete(a, i, cursed, variant):
                    new_cost = dp[i][j] + delete_cost

                    print("Удаление разрешено.")
                    print(
                        f"Стоимость: {format_number(dp[i][j])} + "
                        f"{format_number(delete_cost)} = {format_number(new_cost)}"
                    )
                    print(f"Переход в dp[{i + 1}][{j}]")

                    if new_cost < dp[i + 1][j]:
                        dp[i + 1][j] = new_cost
                        print("Клетка обновлена.")
                    else:
                        print("Клетка не обновлена.")
                else:
                    print("Удаление запрещено из-за проклятого символа.")

            print_dp(dp, a, b)

    print("=" * 60)
    print("Итог:")

    if dp[n][m] == INF:
        print("Преобразование невозможно.")
        print("Impossible")
    else:
        print("Минимальная стоимость преобразования:")
        print(format_number(dp[n][m]))


main()