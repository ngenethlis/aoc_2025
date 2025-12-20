def area(c1,c2):
   
    dx = abs(c1[0] - c2[0])
    dy = abs(c1[1] - c2[1])
    return dx*dy


def sol_p1():
    f = open('data.txt','r')
    lines = [list(map(int,l.strip().split(','))) for l in f.readlines()]
    lines = sorted(lines)
    n = len(lines)
    l1 = lines[:n//2]
    l2 = lines[n//2:]
    
    #print(l1)
    #print(l2)

    max_a = 0
    for p1 in l1:
        for p2 in l2:
            max_a = max(max_a, area(p1,p2))

    return max_a

import sys

# Increase recursion limit for deep flood fills
sys.setrecursionlimit(20000)

def sol_p2_sets():
    # 1. Parse Input
    try:
        with open('data.txt', 'r') as f:
            # We keep the list for the vertex order (the path)
            vertices = [list(map(int, l.strip().split(','))) for l in f.readlines()]
    except FileNotFoundError:
        print("Error: example.txt not found.")
        return 0

    if not vertices:
        return 0

    # 2. Trace the Boundary
    # We use a set for fast O(1) lookups
    boundary_points = set()
    
    num_v = len(vertices)
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    
    # Draw the lines between vertices
    for i in range(num_v):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % num_v] # Wrap around
        
        # Add all points on the segment to the set
        if p1[0] == p2[0]: # Vertical line
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                boundary_points.add((p1[0], y))
        else: # Horizontal line
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                boundary_points.add((x, p1[1]))

    # 3. Identify the "Outside"
    # We define a bounding box with padding to ensure we can reach all outside areas
    min_x, max_x = min(xs) - 1, max(xs) + 1
    min_y, max_y = min(ys) - 1, max(ys) + 1
    
    outside_points = set()
    start_node = (min_x, min_y) # Top-left corner of padded box (guaranteed outside)
    
    # Use a stack for Flood Fill (Iterative DFS) to avoid recursion limits
    stack = [start_node]
    outside_points.add(start_node)
    
    while stack:
        cx, cy = stack.pop()
        
        # Check 4 neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            
            # Stay within our padded bounding box
            if min_x <= nx <= max_x and min_y <= ny <= max_y:
                # If we haven't seen it, AND it's not a boundary wall
                if (nx, ny) not in outside_points and (nx, ny) not in boundary_points:
                    outside_points.add((nx, ny))
                    stack.append((nx, ny))

    # 4. Check Rectangles
    # We iterate all pairs of Red Vertices
    max_area = 0
    
    for i in range(num_v):
        for j in range(i + 1, num_v):
            p1 = vertices[i]
            p2 = vertices[j]
            
            # Define the rectangle boundaries
            x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            
            current_area = (x2 - x1 + 1) * (y2 - y1 + 1)
            
            # Optimization: If this area is smaller than our best so far, skip it
            if current_area <= max_area:
                continue
            
            # Validity Check:
            # The rectangle is valid if NO point inside it belongs to 'outside_points'
            # (Checking boundary_points is not needed because they are valid)
            is_valid = True
            
            # We iterate the rectangle area
            # Note: This can be slow for very large rectangles!
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if (x, y) in outside_points:
                        is_valid = False
                        break # Stop checking this rect immediately
                if not is_valid:
                    break
            
            if is_valid:
                max_area = current_area

    return max_area

print("Largest Area:", sol_p2_sets())
