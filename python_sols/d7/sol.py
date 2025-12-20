from pprint import pprint

def sol_p1():
    f = open("data.txt", 'r')
    grid = [line.rstrip('\n') for line in f.readlines()]

    rows = len(grid)
    cols = len(grid[0])
    
    # find s
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos: break
    
    # beam starts below S
    queue = [(start_pos[0] + 1, start_pos[1])]
    
    # We need to track visited coordinates to handle merging beams
    # and prevent processing the same empty space twice.
    visited_coords = set()
    
    activated_splitters = set()

    while queue:
        r, c = queue.pop(0)

        # boundary check
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
            
        if (r, c) in visited_coords:
            continue
        visited_coords.add((r, c))

        current_char = grid[r][c]

        if current_char == '^':
            activated_splitters.add((r, c))
            
            queue.append((r + 1, c - 1)) # Left branch
            queue.append((r + 1, c + 1)) # Right branch
            
        else:
            queue.append((r + 1, c))

    # 4. Output Result
    print(f"Total splits: {len(activated_splitters)}")

from collections import defaultdict

def sol_p2():
    # 1. Read and Parse
    try:
        with open("data.txt", 'r') as f:
            grid = [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print("Error: data.txt not found.")
        return

    rows = len(grid)
    cols = len(grid[0])
    
    # 2. Find Start
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos: break
        
    if not start_pos:
        print("No start 'S' found!")
        return

    # 3. Initialize Path Counters
    # paths_at[(r, c)] stores the number of distinct timelines active at that coordinate
    paths_at = defaultdict(int)
    
    # We start with 1 timeline at the position S
    paths_at[start_pos] = 1
    
    total_completed_timelines = 0
    
    # 4. Process row by row
    # Since beams always move DOWN (r+1), we can iterate r from top to bottom.
    # This ensures we have fully calculated all incoming paths for row r before moving to r+1.
    for r in range(rows):
        for c in range(cols):
            
            count = paths_at[(r, c)]
            
            # If no beams reached this spot, skip it
            if count == 0:
                continue
            
            char = grid[r][c]
            
            # Determine where the beams go next
            next_positions = []
            
            if char == '^':
                # Splitter: Creates two timelines, one left-down, one right-down
                next_positions.append((r + 1, c - 1))
                next_positions.append((r + 1, c + 1))
            else:
                # Empty '.' or Start 'S': Continues straight down
                next_positions.append((r + 1, c))
                
            # Distribute the counts to the next positions
            for nr, nc in next_positions:
                # Check if the beam exits the manifold
                if nr >= rows or nc < 0 or nc >= cols:
                    total_completed_timelines += count
                else:
                    # Accumulate paths at the next position
                    paths_at[(nr, nc)] += count

    # 5. Output
    print(f"Total active timelines: {total_completed_timelines}")


sol_p2()
