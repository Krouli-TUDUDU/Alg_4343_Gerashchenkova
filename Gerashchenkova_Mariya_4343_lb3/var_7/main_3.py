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

    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue

            # M — символы совпали, ничего не делаем
            if i < n and j < m and a[i] == b[j]:
                dp[i + 1][j + 1] = min(
                    dp[i + 1][j + 1],
                    dp[i][j]
                )

            # R — заменить символ первой строки
            if i < n and j < m and a[i] != b[j]:
                if can_replace(a, i, cursed, variant):
                    dp[i + 1][j + 1] = min(
                        dp[i + 1][j + 1],
                        dp[i][j] + 1
                    )

            # I — вставить символ второй строки
            if j < m:
                dp[i][j + 1] = min(
                    dp[i][j + 1],
                    dp[i][j] + 1
                )

            # D — удалить символ первой строки
            if i < n:
                if can_delete(a, i, cursed, variant):
                    dp[i + 1][j] = min(
                        dp[i + 1][j],
                        dp[i][j] + 1
                    )

    if dp[n][m] == INF:
        print("Impossible")
    else:
        print(dp[n][m])

main()