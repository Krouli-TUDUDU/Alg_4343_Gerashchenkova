import sys


def debug(*args):
    print(*args, file=sys.stderr)


def solve_alsh2():
    data = []
    try:
        while True:
            data.extend(input().split())
    except EOFError:
        pass

    if not data:
        return

    n = int(data[0])

    matrix = []
    idx = 1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(data[idx]))
            idx += 1
        matrix.append(row)

    debug("Количество вершин:", n)
    debug("Матрица смежности:")
    for row in matrix:
        debug(row)

    visited = [False] * n

    current_node = 0
    visited[current_node] = True
    path = [current_node]
    total_cost = 0

    debug("Стартуем из вершины 0")
    debug("Начальный путь:", path)
    debug("Начальная стоимость:", total_cost)

    for step in range(n - 1):
        debug()
        debug(f"Шаг {step + 1}")
        debug("Текущая вершина:", current_node)
        debug("Посещённые вершины:", visited)

        next_node = -1
        min_dist = float('inf')

        for v in range(n):
            debug(f"Проверяем вершину {v}")

            if not visited[v] and matrix[current_node][v] > 0:
                debug(
                    f"Можно перейти {current_node} -> {v}, "
                    f"вес = {matrix[current_node][v]}"
                )

                if matrix[current_node][v] < min_dist:
                    debug(
                        f"Это лучший вариант на данный момент: "
                        f"{matrix[current_node][v]} < {min_dist}"
                    )
                    min_dist = matrix[current_node][v]
                    next_node = v
            else:
                debug(
                    f"Переход {current_node} -> {v} невозможен "
                    f"или вершина уже посещена"
                )

        if next_node == -1:
            debug("Не удалось найти следующую вершину")
            print("no path")
            return

        visited[next_node] = True
        path.append(next_node)
        total_cost += min_dist
        current_node = next_node

        debug("Выбрана вершина:", next_node)
        debug("Добавленная стоимость:", min_dist)
        debug("Текущий путь:", path)
        debug("Текущая стоимость:", total_cost)

    debug()
    debug("Все вершины посещены")
    debug("Проверяем возможность вернуться в вершину 0")

    if matrix[current_node][0] > 0:
        debug(
            f"Можно вернуться {current_node} -> 0, "
            f"вес = {matrix[current_node][0]}"
        )

        total_cost += matrix[current_node][0]
        path.append(0)

        debug("Итоговая стоимость:", total_cost)
        debug("Итоговый путь:", path)

        print(f"{total_cost} " + " ".join(map(str, path)))
    else:
        debug(f"Нет ребра из {current_node} в 0")
        print("no path")


solve_alsh2()