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


def calculate_area(p1, p2):
    # Area based on tile count (inclusive coordinates)
    # Example: 2,5 to 9,7 is dx=7, dy=2 -> 8 * 3 = 24 area
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def is_on_segment(p, a, b):
    # Check if point p is exactly on the segment a-b
    x, y = p
    x1, y1 = a
    x2, y2 = b
    
    # Vertical segment
    if x1 == x2:
        return x == x1 and min(y1, y2) <= y <= max(y1, y2)
    # Horizontal segment
    elif y1 == y2:
        return y == y1 and min(x1, x2) <= x <= max(x1, x2)
    return False

def is_inside_polygon(p, vertices):
    # Check if a point is Inside or On Boundary of the rectilinear polygon
    
    # 1. Quick check: Is point exactly on any boundary edge?
    n = len(vertices)
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        if is_on_segment(p, p1, p2):
            return True

    # 2. Ray Casting (Ray to positive X)
    # If not on boundary, determine if inside by counting edge crossings
    x, y = p
    intersections = 0
    
    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]
        
        # Only check vertical edges for a horizontal ray
        if v1[0] == v2[0]:
            edge_x = v1[0]
            edge_y_min = min(v1[1], v2[1])
            edge_y_max = max(v1[1], v2[1])
            
            # The edge must be strictly to the right
            if edge_x > x:
                # Standard Point-in-Poly rule: include lower y, exclude upper y
                if edge_y_min <= y < edge_y_max:
                    intersections += 1
                    
    return (intersections % 2) == 1

def rect_intersects_polygon_edges(r_min_x, r_max_x, r_min_y, r_max_y, vertices):
    # Check if any polygon edge strictly cuts through the rectangle
    
    is_thin_rect_x = (r_min_x == r_max_x)
    is_thin_rect_y = (r_min_y == r_max_y)
    
    n = len(vertices)
    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]
        
        # --- Handle Vertical Polygon Edges ---
        if v1[0] == v2[0]:
            edge_x = v1[0]
            edge_y_min = min(v1[1], v2[1])
            edge_y_max = max(v1[1], v2[1])
            
            # Check if this vertical edge cuts the rectangle
            if r_min_x < edge_x < r_max_x:
                if is_thin_rect_y:
                    # For a horizontal line rect, strict crossing is bad
                    if edge_y_min < r_min_y < edge_y_max:
                        return True
                else:
                    # For a 2D rect, overlap of Y-intervals is bad
                    overlap_min = max(edge_y_min, r_min_y)
                    overlap_max = min(edge_y_max, r_max_y)
                    if overlap_min < overlap_max:
                        return True

        # --- Handle Horizontal Polygon Edges ---
        elif v1[1] == v2[1]:
            edge_y = v1[1]
            edge_x_min = min(v1[0], v2[0])
            edge_x_max = max(v1[0], v2[0])
            
            # Check if this horizontal edge cuts the rectangle
            if r_min_y < edge_y < r_max_y:
                if is_thin_rect_x:
                    # For a vertical line rect, strict crossing is bad
                    if edge_x_min < r_min_x < edge_x_max:
                        return True
                else:
                    # For a 2D rect, overlap of X-intervals is bad
                    overlap_min = max(edge_x_min, r_min_x)
                    overlap_max = min(edge_x_max, r_max_x)
                    if overlap_min < overlap_max:
                        return True
                    
    return False

def solve():
    try:
        f = open('data.txt', 'r')
    except FileNotFoundError:
        print("Error: data.txt not found.")
        return

    # Parse coordinates. 
    # CRITICAL: Keep original order. The list order defines the polygon loop.
    points = [list(map(int, l.strip().split(','))) for l in f if l.strip()]
    f.close()
    
    n = len(points)
    max_a = 0
    
    # Iterate all pairs of red tiles
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            
            # 1. Calculate potential area
            current_area = calculate_area(p1, p2)
            
            # Optimization: Skip expensive checks if area isn't an improvement
            if current_area <= max_a:
                continue
            
            # 2. Determine Rectangle Bounds
            r_min_x, r_max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
            r_min_y, r_max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
            
            # 3. Check Implicit Corners
            # The rectangle is defined by p1, p2 and two implicit corners c1, c2.
            # We must verify c1 and c2 are valid (Green or Red).
            c1 = (r_min_x, r_max_y)
            c2 = (r_max_x, r_min_y)
            
            if not is_inside_polygon(c1, points) or not is_inside_polygon(c2, points):
                continue
            
            # 4. Check Interior Intersection
            # Ensure no polygon boundary cuts through the rectangle
            if rect_intersects_polygon_edges(r_min_x, r_max_x, r_min_y, r_max_y, points):
                continue
                
            # If we passed all checks, this is a valid new maximum
            max_a = current_area

    print(f"Max Area: {max_a}")
    return max_a

if __name__ == '__main__':
    solve()

