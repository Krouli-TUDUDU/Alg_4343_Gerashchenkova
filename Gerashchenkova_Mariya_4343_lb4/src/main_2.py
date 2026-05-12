import sys
from array import array


def prefix_function(p):
    n = len(p)
    pi = array('I', [0]) * n

    for i in range(1, n):
        j = pi[i - 1]

        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]

        if p[i] == p[j]:
            j += 1

        pi[i] = j

    return pi


def kmp_cyclic_shift(A, B):
    n = len(A)

    if n != len(B):
        return -1

    if n == 0:
        return 0

    pi = prefix_function(B)
    j = 0


    for i in range(2 * n - 1):
        c = A[i % n]

        while j > 0 and c != B[j]:
            j = pi[j - 1]

        if c == B[j]:
            j += 1

        if j == n:
            start = i - n + 1

            if start < n:
                return start

            j = pi[j - 1]

    return -1


A = sys.stdin.readline().rstrip('\n')
B = sys.stdin.readline().rstrip('\n')

print(kmp_cyclic_shift(A, B))