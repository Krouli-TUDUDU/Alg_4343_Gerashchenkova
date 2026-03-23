class TraceLogger:
    def __init__(self, enabled=False, filename="trace.txt"):
        self.enabled = enabled
        self.file = open(filename, "w", encoding="utf-8") if enabled else None

    def log(self, text=""):
        if not self.enabled:
            return
        print(text)
        if self.file is not None:
            self.file.write(text + "\n")

    def close(self):
        if self.file is not None:
            self.file.close()


def first_info(h, n):
    min_h = h[0]
    pos = 0
    for i in range(1, n):
        if h[i] < min_h:
            min_h = h[i]
            pos = i

    run = 1
    i = pos + 1
    while i < n and h[i] == min_h:
        run += 1
        i += 1

    max_size = run
    down = n - min_h
    if max_size > down:
        max_size = down

    return pos, min_h, max_size


def greedy_bound(n):
    h = [0] * n
    placed = []

    while True:
        pos, min_h, max_size = first_info(h, n)
        if min_h == n:
            return placed

        s = max_size
        if not placed and s == n:
            s -= 1

        for j in range(pos, pos + s):
            h[j] += s

        placed.append((min_h, pos, s))


def format_solution(sol):
    return [(r + 1, c + 1, s) for r, c, s in sol]


def solve(n, trace=False):
    logger = TraceLogger(trace)

    if n % 2 == 0:
        s = n // 2
        ans = [
            (0, 0, s),
            (0, s, s),
            (s, 0, s),
            (s, s, s)
        ]
        logger.log("Четный N, используется прямое разбиение.")
        logger.log("Ответ:")
        for x, y, w in format_solution(ans):
            logger.log(f"{x} {y} {w}")
        logger.close()
        return ans

    heights = [0] * n
    current = []
    best = greedy_bound(n)
    best_count = len(best)
    total = n * n
    filled = 0
    memo = {}
    step = 0

    pos, h, max_size = first_info(heights, n)
    if max_size == n:
        max_size -= 1

    stack = [[pos, h, max_size, n // 2 + 1, -1, -1, -1]]

    logger.log("Начало работы алгоритма")
    logger.log(f"N = {n}")
    logger.log(f"Начальная верхняя граница: {best_count}")
    logger.log(f"Начальные heights: {heights}")
    logger.log("")

    while stack:
        pos, h, next_size, min_size, pr, pc, ps = stack[-1]

        if next_size < min_size:
            logger.log("Варианты в текущем состоянии закончились, выполняется возврат")
            stack.pop()
            if ps != -1:
                for j in range(pc, pc + ps):
                    heights[j] -= ps
                filled -= ps * ps
                removed = current.pop()
                logger.log(f"Откат квадрата: ({removed[0] + 1}, {removed[1] + 1}, {removed[2]})")
                logger.log(f"heights после отката: {heights}")
                logger.log("")
            continue

        s = next_size
        stack[-1][2] = next_size - 1

        for j in range(pos, pos + s):
            heights[j] += s
        filled += s * s
        current.append((h, pos, s))
        used = len(current)
        step += 1

        logger.log(f"Шаг {step}")
        logger.log(f"Пробуем квадрат: ({h + 1}, {pos + 1}, {s})")
        logger.log(f"Текущее решение: {format_solution(current)}")
        logger.log(f"heights: {heights}")
        logger.log(f"Заполненная площадь: {filled} из {total}")

        prune = False

        if filled == total:
            logger.log("Поле заполнено полностью")
            if used < best_count:
                best_count = used
                best = current[:]
                logger.log(f"Найдено новое лучшее решение: {best_count} квадратов")
                logger.log(f"Лучшее решение: {format_solution(best)}")
            prune = True

        elif used >= best_count:
            logger.log("Отсечение: текущее число квадратов не лучше лучшего найденного")
            prune = True

        else:
            _, min_h, _ = first_info(heights, n)
            remain = total - filled
            max_possible = n - min_h
            low = (remain + max_possible * max_possible - 1) // (max_possible * max_possible)

            logger.log(f"Оставшаяся площадь: {remain}")
            logger.log(f"Нижняя оценка оставшихся квадратов: {low}")

            if used + low >= best_count:
                logger.log("Отсечение по нижней оценке")
                prune = True
            else:
                key = tuple(heights)
                prev = memo.get(key)
                if prev is not None and prev <= used:
                    logger.log("Отсечение: такое состояние уже встречалось раньше не хуже")
                    prune = True
                else:
                    memo[key] = used
                    logger.log("Состояние сохранено в memo")

        if prune:
            removed = current.pop()
            filled -= s * s
            for j in range(pos, pos + s):
                heights[j] -= s
            logger.log(f"Откат квадрата: ({removed[0] + 1}, {removed[1] + 1}, {removed[2]})")
            logger.log(f"heights после отката: {heights}")
            logger.log("")
            continue

        pos2, h2, max_size2 = first_info(heights, n)
        stack.append([pos2, h2, max_size2, 1, h, pos, s])

        logger.log("Переход на следующий уровень поиска")
        logger.log(f"Следующая позиция: строка {h2 + 1}, столбец {pos2 + 1}")
        logger.log(f"Максимальный размер следующего квадрата: {max_size2}")
        logger.log("")

    logger.log("Поиск завершен")
    logger.log(f"Лучший ответ: {best_count} квадратов")
    for x, y, w in format_solution(best):
        logger.log(f"{x} {y} {w}")
    logger.close()

    return best


n = int(input())
trace = True
ans = solve(n, trace)

print(len(ans))
for r, c, s in ans:
    print(r + 1, c + 1, s)

