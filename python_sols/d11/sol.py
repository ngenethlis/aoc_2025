# list of dev: out1 out2 ...
# count num of paths from you to out

from collections import defaultdict
from functools import lru_cache



def count_paths(connections, start = 'you', required = set() ):
    end = 'out'
    
    @lru_cache
    def dfs(current, visited):
        # Base Case: We reached the end
        if current == end:
            if (required.issubset(visited)):
                return 1
        
        # Mark current node as visited for this path
        visited.add(current)
        
        path_count = 0
        
        # Check all neighbors
        for neighbor in connections[current]:
            # Only go to neighbors we haven't visited in this specific path
            if neighbor not in visited:
                path_count += dfs(neighbor, visited)
        
        # Backtrack: Unmark current node so other paths can use it
        visited.remove(current)
        
        return path_count

    # Start the search with an empty visited set
    return dfs(start, set())

def sol_p1():
    f = open("data.txt",'r')
    connections = defaultdict(set)
    for l in f.readlines():
        inp, out = l.split(':')
        inp = inp.strip()
        out = out.split()
        connections[inp].update(out)
    
    return count_paths(connections)


def count_paths_p2(connections, start='svr', required={'dac', 'fft'}):
    end = 'out'
    required = frozenset(required) # Must be immutable for caching

    # Logic: State = (current_node, remaining_requirements)
    @lru_cache(None)
    def solve(current, to_visit):
        # 1. Base Case: Reached the end
        if current == end:
            # Only count as 1 if we have NO required nodes left to visit
            return 1 if not to_visit else 0
        
        count = 0
        
        # 2. Check neighbors
        for neighbor in connections[current]:
            # Update the 'to_visit' set for the next step
            # If the neighbor is one of the required ones, remove it from the set
            new_to_visit = to_visit
            if neighbor in to_visit:
                new_to_visit = to_visit - {neighbor}
            
            count += solve(neighbor, new_to_visit)
            
        return count

    # Start: Check if 'start' itself is a required node
    initial_to_visit = required
    if start in required:
        initial_to_visit = required - {start}

    return solve(start, initial_to_visit)

def sol_p2():
    f = open("data.txt",'r')
    connections = defaultdict(set)
    for l in f.readlines():
        inp, out = l.split(':')
        inp = inp.strip()
        out = out.split()
        connections[inp].update(out)
    
    return count_paths_p2(connections)

print(sol_p2())
