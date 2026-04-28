import sys


def debug(*args):
    print(*args, file=sys.stderr)


def solve():
    input_data = []
    try:
        while True:
            input_data.extend(input().split())
    except EOFError:
        pass

    if not input_data:
        return

    n = int(input_data[0])

    matrix = []
    idx = 1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(input_data[idx]))
            idx += 1
        matrix.append(row)

    debug("Количество вершин:", n)
    debug("Матрица смежности:")
    for row in matrix:
        debug(row)

    INF = float('inf')

    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    dp[1][0] = 0

    debug("Начинаем динамическое программирование")
    debug("dp[1][0] = 0, стартуем из вершины 0")

    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue

        for u in range(n):
            if (mask & (1 << u)) and dp[mask][u] != INF:
                debug()
                debug(f"Текущая маска: {bin(mask)}, последняя вершина: {u}")
                debug(f"Текущая стоимость пути: {dp[mask][u]}")

                for v in range(n):
                    if not (mask & (1 << v)) and matrix[u][v] > 0:
                        new_mask = mask | (1 << v)
                        new_cost = dp[mask][u] + matrix[u][v]

                        debug(
                            f"Пробуем перейти {u} -> {v}, "
                            f"вес = {matrix[u][v]}, новая стоимость = {new_cost}"
                        )

                        if new_cost < dp[new_mask][v]:
                            debug(
                                f"Обновляем dp[{bin(new_mask)}][{v}]: "
                                f"{dp[new_mask][v]} -> {new_cost}"
                            )
                            dp[new_mask][v] = new_cost
                            parent[new_mask][v] = u
                        else:
                            debug("Не обновляем, потому что уже есть путь дешевле")

    full_mask = (1 << n) - 1
    ans = INF
    last_node = -1

    debug()
    debug("Все вершины должны быть посещены")
    debug("Полная маска:", bin(full_mask))
    debug("Проверяем возврат в начальную вершину 0")

    for u in range(1, n):
        if dp[full_mask][u] != INF and matrix[u][0] > 0:
            cost = dp[full_mask][u] + matrix[u][0]

            debug(
                f"Последняя вершина {u}: "
                f"стоимость пути = {dp[full_mask][u]}, "
                f"возврат {u} -> 0 = {matrix[u][0]}, "
                f"итог = {cost}"
            )

            if cost < ans:
                debug(f"Найден новый лучший ответ: {cost}")
                ans = cost
                last_node = u

    if ans == INF:
        debug("Гамильтонов цикл не найден")
        print("no path")
    else:
        debug()
        debug("Восстанавливаем путь")

        path = [0]
        curr_mask = full_mask
        curr_node = last_node

        while curr_node != 0:
            path.append(curr_node)
            next_node = parent[curr_mask][curr_node]

            debug(
                f"Текущая вершина: {curr_node}, "
                f"предыдущая вершина: {next_node}, "
                f"маска: {bin(curr_mask)}"
            )

            curr_mask ^= (1 << curr_node)
            curr_node = next_node

        path.append(0)
        path.reverse()

        debug("Итоговая стоимость:", ans)
        debug("Итоговый путь:", path)

        print(ans)
        print(" ".join(map(str, path)))


solve()