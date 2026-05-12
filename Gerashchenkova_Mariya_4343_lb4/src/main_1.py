def prefix_function(p):
    n = len(p)
    pi = [0] * n

    for i in range(1, n):
        j = pi[i - 1]

        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]

        if p[i] == p[j]:
            j += 1

        pi[i] = j

    return pi


def kmp_search(pattern, text):
    pi = prefix_function(pattern)
    result = []
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            result.append(i - len(pattern) + 1)
            j = pi[j - 1]

    return result


P = input().strip()
T = input().strip()

ans = kmp_search(P, T)

if ans:
    print(",".join(map(str, ans)))
else:
    print(-1)