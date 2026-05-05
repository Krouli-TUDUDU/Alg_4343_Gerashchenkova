INF = 10 ** 18


def format_number(x):
    if abs(x - int(x)) < 1e-9:
        return str(int(x))
    return str(x)



replace_cost, insert_cost, delete_cost = map(float, input().split())

a = input().strip()
b = input().strip()

n = len(a)
m = len(b)

dp = [[INF] * (m + 1) for _ in range(n + 1)]

dp[0][0] = 0

for i in range(n + 1):
    for j in range(m + 1):
        if i < n and j < m:
            if a[i] == b[j]:
                dp[i + 1][j + 1] = min(dp[i + 1][j + 1], dp[i][j])
            else:
                dp[i + 1][j + 1] = min(dp[i + 1][j + 1], dp[i][j] + replace_cost)

        if j < m:
            dp[i][j + 1] = min(dp[i][j + 1], dp[i][j] + insert_cost)

        if i < n:
            dp[i + 1][j] = min(dp[i + 1][j], dp[i][j] + delete_cost)

print(format_number(dp[n][m]))

