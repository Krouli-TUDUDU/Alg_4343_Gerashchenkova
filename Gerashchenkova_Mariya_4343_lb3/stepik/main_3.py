s = input().strip()
t = input().strip()

n = len(s)
m = len(t)

if m > n:
    s, t = t, s
    n, m = m, n

previous = list(range(m + 1))

for i in range(1, n + 1):
    current = [0] * (m + 1)
    current[0] = i

    for j in range(1, m + 1):
        if s[i - 1] == t[j - 1]:
            current[j] = previous[j - 1]
        else:
            current[j] = min(
                previous[j] + 1,      
                current[j - 1] + 1,   
                previous[j - 1] + 1   
            )

    previous = current

print(previous[m])