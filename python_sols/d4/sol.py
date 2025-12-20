from pprint import pprint

def sol_p1():
    with open("data.txt") as f:
        grid = [list(l.replace('.', '0').replace('@', '1')) for l in f.read().splitlines()]

    total = 0
    R, C = len(grid), len(grid[0])

    # 8 directions around a cell
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    for r in range(R):
        for c in range(C):
            if grid[r][c] != '1':
                continue

            neighbors = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    neighbors.append(grid[nr][nc])

            if sum(map(int, neighbors)) < 4:
                total += 1

    return total

def sol_p2():
    with open("data.txt") as f:
        grid = [list(l.replace('.', '0').replace('@', '1')) for l in f.read().splitlines()]

    total = 0
    total_changed = True
    R, C = len(grid), len(grid[0])

    # 8 directions around a cell
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    while (total_changed):
        total_changed = False

        for r in range(R):
            for c in range(C):
                if grid[r][c] != '1':
                    continue

                neighbors = []
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C:
                        neighbors.append(grid[nr][nc])

                if sum(map(int, neighbors)) < 4:
                    total += 1
                    total_changed = True
                    grid[r][c] = '0'
    
    print(grid)
    pprint(grid)
    return total



print(sol_p2())
