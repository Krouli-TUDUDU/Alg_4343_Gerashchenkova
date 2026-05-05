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
parent = [[None] * (m + 1) for _ in range(n + 1)]

dp[0][0] = 0

for i in range(n + 1):
    for j in range(m + 1):
        current = dp[i][j]

        if i < n and j < m:
            if a[i] == b[j]:
                new_cost = current
                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    parent[i + 1][j + 1] = (i, j, "M")
            else:
                new_cost = current + replace_cost
                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    parent[i + 1][j + 1] = (i, j, "R")

        if j < m:
            new_cost = current + insert_cost
            if new_cost < dp[i][j + 1]:
                dp[i][j + 1] = new_cost
                parent[i][j + 1] = (i, j, "I")

        if i < n:
            new_cost = current + delete_cost
            if new_cost < dp[i + 1][j]:
                dp[i + 1][j] = new_cost
                parent[i + 1][j] = (i, j, "D")

operations = []

i = n
j = m

while i > 0 or j > 0:
    prev_i, prev_j, op = parent[i][j]
    operations.append(op)
    i, j = prev_i, prev_j

operations.reverse()

print("".join(operations))
print(a)
print(b)


