def Solve(N):
    h = [0] * N
    best_tiles = []
    tile = []

    seen = {}

    def pack(arr):
        key = 0
        base = N + 1
        for v in arr:
            key = key * base + v
        return key

    def Big_k(N):
        hh = h[:]
        tt = []
        while True:
            mh = hh[0]
            x = 0
            for i in range(1, N):
                if hh[i] < mh:
                    mh = hh[i]
                    x = i
            if mh == N:
                break

            y = mh

            maxw = 0
            while x + maxw < N and hh[x + maxw] == mh:
                maxw += 1

            k = min(maxw, N - y)
            if x == 0 and y == 0 and k == N:
                k = N - 1

            for i in range(x, x + k):
                hh[i] += k
            tt.append((x + 1, y + 1, k))

        return len(tt), tt

    best_k, best_tiles = Big_k(N)

    max_sq_area = (N - 1) * (N - 1)
    total_area = N * N

    def great(u, filled):
        nonlocal best_k, best_tiles
        if u >= best_k:
            return

        if u <= 10:
            key = pack(h)
            prev = seen.get(key)
            if prev is not None and u >= prev:
                return
            seen[key] = u

        if filled == total_area:
            best_k = u
            best_tiles = tile[:]
            return

        area_left = total_area - filled
        lb = (area_left + max_sq_area - 1) // max_sq_area
        if u + lb >= best_k:
            return

        mn = h[0]
        x = 0
        for i in range(1, N):
            if h[i] < mn:
                mn = h[i]
                x = i
        y = mn

        maxw = 0
        while x + maxw < N and h[x + maxw] == mn:
            maxw += 1

        max_size = min(maxw, N - y)
        if x == 0 and y == 0 and max_size == N:
            max_size = N - 1

        for k in range(max_size, 0, -1):
            for c in range(x, x + k):
                h[c] += k
            tile.append((x + 1, y + 1, k))

            great(u + 1, filled + k * k)

            tile.pop()
            for c in range(x, x + k):
                h[c] -= k

    great(0, 0)

    print(best_k)
    for t in best_tiles:
        print(*t)


N = int(input())
Solve(N)
