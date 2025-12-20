from collections import deque
import math

def dist(p1,p2):
    return math.sqrt(
        (p1[0] - p2[0])**2 + 
        (p1[1] - p2[1])**2 + 
        (p1[2] - p2[2])**2
    )


def sol_p1():
    f = open("data.txt", 'r')
    pos = [tuple(map(int, l.strip().split(','))) for l in f.readlines()]
    
    edges = []
    num_boxes = len(pos)
    
    for i in range(num_boxes):
        for j in range(i + 1, num_boxes):
            p1 = pos[i]
            p2 = pos[j]
            
            dist_sq = dist(p1,p2)
            edges.append((dist_sq, i, j))

    # 3. Sort edges by distance (ascending)
    edges.sort(key=lambda x: x[0])

    # 4. Union-Find (DSU) Data Structure Setup
    parent = list(range(num_boxes))
    # Every box starts as a circuit of size 1
    sizes = [1] * num_boxes 

    def find(i):
        # Path compression for efficiency
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        
        if root_i != root_j:
            # Merge smaller into larger (optional optimization, but good practice)
            if sizes[root_i] < sizes[root_j]:
                root_i, root_j = root_j, root_i
            
            parent[root_j] = root_i
            sizes[root_i] += sizes[root_j]
            # Zero out the size of the child to avoid double counting later
            sizes[root_j] = 0
            return True # Merged occurred
        return False # Already connected

    limit = len(pos) # for act data
    
    for k in range(min(limit, len(edges))):
        _, u, v = edges[k]
        union(u, v)

    # 6. Get results
    # Filter out sizes of 0 (which represent boxes that were merged into others)
    final_circuit_sizes = [s for s in sizes if s > 0]
    
    # Sort sizes descending to find the largest ones
    final_circuit_sizes.sort(reverse=True)
    
    result = final_circuit_sizes[0] * final_circuit_sizes[1] * final_circuit_sizes[2]
    print(f"\nResult (product of top 3): {result}")


def sol_p2():
    # 1. Parse Input
    f = open("example.txt", 'r')
    boxes = [tuple(map(int, l.strip().split(','))) for l in f.readlines()]
    num_boxes = len(boxes)
    if num_boxes < 2:
        print("Not enough boxes to form connections.")
        return

    # 2. Generate all pairs and calculate squared distances
    edges = []
    for i in range(num_boxes):
        for j in range(i + 1, num_boxes):
            p1 = boxes[i]
            p2 = boxes[j]
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            edges.append((dist_sq, i, j))

    # 3. Sort edges by distance (ascending)
    edges.sort(key=lambda x: x[0])

    # 4. Union-Find (DSU) Setup
    parent = list(range(num_boxes))
    # We track the number of distinct clusters (circuits).
    # Initially, every box is its own cluster.
    num_clusters = num_boxes 

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        
        if root_i != root_j:
            parent[root_j] = root_i
            return True # A merge happened
        return False # Already in same circuit

    # 5. Process edges until we have exactly 1 circuit left
    for dist, u, v in edges:
        if union(u, v):
            num_clusters -= 1
            
            # Check if this was the final connection needed
            if num_clusters == 1:
                x1 = boxes[u][0]
                x2 = boxes[v][0]
                result = x1 * x2
                
                print(f"Graph unified! Last connection between index {u} and {v}.")
                print(f"Box 1: {boxes[u]}")
                print(f"Box 2: {boxes[v]}")
                print(f"Result (X1 * X2): {result}")
                return result

print(sol_p2())
