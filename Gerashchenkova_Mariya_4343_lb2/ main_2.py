def solve_alsh2():
    data = []
    try:
        while True:
            data.extend(input().split())
    except EOFError:
        pass
        
    if not data:
        return
        
    n = int(data[0])
    
    matrix = []
    idx = 1
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(data[idx]))
            idx += 1
        matrix.append(row)
        
    visited = [False] * n
    
    current_node = 0
    visited[current_node] = True
    path = [current_node]
    total_cost = 0
    
    for _ in range(n - 1):
        next_node = -1
        min_dist = float('inf')
        
        # Ищем ближайший непосещенный город
        for v in range(n):
            if not visited[v] and matrix[current_node][v] > 0:
                if matrix[current_node][v] < min_dist:
                    min_dist = matrix[current_node][v]
                    next_node = v
                    
        if next_node == -1:
            print("no path")
            return
            
        # Переходим в найденный ближайший город
        visited[next_node] = True
        path.append(next_node)
        total_cost += min_dist
        current_node = next_node
        
    #Попытка вернуться в стартовый город (0) для замыкания цикла
    if matrix[current_node][0] > 0:
        total_cost += matrix[current_node][0]
        path.append(0)
        print(f"{total_cost} " + " ".join(map(str, path)))
    else:
        print("no path")

solve_alsh2()