def solve():
    input_data = []
    try:
        while True:
            input_data.extend(input().split())
    except EOFError:
        pass
    if not input_data:
        return
    
    n = int(input_data[0])
    
    matrix = []
    idx = 1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(input_data[idx]))
            idx += 1
        matrix.append(row)
        
    INF = float('inf')
    
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    
    dp[1][0] = 0
    
    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue
        
        for u in range(n):
            if (mask & (1 << u)) and dp[mask][u] != INF:
                for v in range(n):
                    if not (mask & (1 << v)) and matrix[u][v] > 0:
                        new_mask = mask | (1 << v)
                        new_cost = dp[mask][u] + matrix[u][v]
                        
                        if new_cost < dp[new_mask][v]:
                            dp[new_mask][v] = new_cost
                            parent[new_mask][v] = u
                            
    full_mask = (1 << n) - 1
    ans = INF
    last_node = -1
    
    for u in range(1, n):
        if dp[full_mask][u] != INF and matrix[u][0] > 0:
            cost = dp[full_mask][u] + matrix[u][0]
            if cost < ans:
                ans = cost
                last_node = u
                
    if ans == INF:
        print("no path")
    else:
        path = [0]
        curr_mask = full_mask
        curr_node = last_node
        
        while curr_node != 0:
            path.append(curr_node)
            next_node = parent[curr_mask][curr_node]
            curr_mask ^= (1 << curr_node)
            curr_node = next_node
            
        path.append(0)
        path.reverse()
        
        print(ans)
        print( " ".join(map(str, path)))


solve()




