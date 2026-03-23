def first_info(h, n):
    min_h = h[0]
    pos = 0
    for i in range(1, n):
        v = h[i]
        if v < min_h:
            min_h = v
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


def solve(n):
    if n % 2 == 0:
        s = n // 2
        return [
            (0, 0, s),
            (0, s, s),
            (s, 0, s),
            (s, s, s)
        ]

    heights = [0] * n
    current = []
    best = greedy_bound(n)
    best_count = len(best)
    total = n * n
    filled = 0
    memo = {}

    pos, h, max_size = first_info(heights, n)
    if max_size == n:
        max_size -= 1

    stack = [[pos, h, max_size, n // 2 + 1, -1, -1, -1]]

    while stack:
        pos, h, next_size, min_size, pr, pc, ps = stack[-1]

        if next_size < min_size:
            stack.pop()
            if ps != -1:
                for j in range(pc, pc + ps):
                    heights[j] -= ps
                filled -= ps * ps
                current.pop()
            continue

        s = next_size
        stack[-1][2] = next_size - 1

        for j in range(pos, pos + s):
            heights[j] += s
        filled += s * s
        current.append((h, pos, s))
        used = len(current)

        prune = False

        if filled == total:
            if used < best_count:
                best_count = used
                best = current[:]
            prune = True
        elif used >= best_count:
            prune = True
        else:
            _, min_h, _ = first_info(heights, n)
            remain = total - filled
            max_possible = n - min_h
            low = (remain + max_possible * max_possible - 1) // (max_possible * max_possible)

            if used + low >= best_count:
                prune = True
            else:
                key = tuple(heights)
                prev = memo.get(key)
                if prev is not None and prev <= used:
                    prune = True
                else:
                    memo[key] = used

        if prune:
            current.pop()
            filled -= s * s
            for j in range(pos, pos + s):
                heights[j] -= s
            continue

        pos2, h2, max_size2 = first_info(heights, n)
        stack.append([pos2, h2, max_size2, 1, h, pos, s])

    return best


n = int(input())
ans = solve(n)

print(len(ans))
for r, c, s in ans:
    print(r + 1, c + 1, s)