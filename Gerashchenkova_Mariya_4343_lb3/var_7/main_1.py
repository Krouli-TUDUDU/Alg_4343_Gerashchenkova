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
    parent = [[None] * (m + 1) for _ in range(n + 1)]

    dp[0][0] = 0

    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue

            # M — символы совпали
            if i < n and j < m and a[i] == b[j]:
                new_cost = dp[i][j]

                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    parent[i + 1][j + 1] = (i, j, "M")

            # R — замена символа
            if i < n and j < m and a[i] != b[j]:
                if can_replace(a, i, cursed, variant):
                    new_cost = dp[i][j] + replace_cost

                    if new_cost < dp[i + 1][j + 1]:
                        dp[i + 1][j + 1] = new_cost
                        parent[i + 1][j + 1] = (i, j, "R")

            # I — вставка символа
            if j < m:
                new_cost = dp[i][j] + insert_cost

                if new_cost < dp[i][j + 1]:
                    dp[i][j + 1] = new_cost
                    parent[i][j + 1] = (i, j, "I")

            # D — удаление символа
            if i < n:
                if can_delete(a, i, cursed, variant):
                    new_cost = dp[i][j] + delete_cost

                    if new_cost < dp[i + 1][j]:
                        dp[i + 1][j] = new_cost
                        parent[i + 1][j] = (i, j, "D")

    if dp[n][m] == INF:
        print("Impossible")
        return

    operations = []

    i = n
    j = m

    while i > 0 or j > 0:
        prev_i, prev_j, op = parent[i][j]

        operations.append(op)

        i = prev_i
        j = prev_j

    operations.reverse()

    print("".join(operations))
    print(a)
    print(b)


main()