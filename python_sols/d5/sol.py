def sol_p1():
    f = open("data.txt", 'r')
    
    fresh_intervals = []
    total_fresh = 0
    lines = f.read().splitlines()
    i = 0 
    for i,line in enumerate(lines):
        if (line == ''):
            break
        l, r = map(int, line.split('-'))
        fresh_intervals.append((l,r))
    
    fresh_intervals.sort()
    fresh = 0

    for j in range(i+1,len(lines)):
        x = int(lines[j])
        if (any(l<=x <=r for l,r in fresh_intervals)):
            fresh+=1

    return fresh

def sol_p2():
    f = open("data.txt", 'r')
    
    fresh_intervals = []
    total_fresh = 0
    lines = f.read().splitlines()
    i = 0 
    for i,line in enumerate(lines):
        if (line == ''):
            break
        l, r = map(int, line.split('-'))
        fresh_intervals.append((l,r))
    
    fresh_intervals.sort()
    
    merged = []
    for l, r in fresh_intervals:
        if not merged or l > merged[-1][1] + 1:
            merged.append([l, r])
        else:
            merged[-1][1] = max(merged[-1][1], r)

    # Count total unique numbers
    total = 0
    for l, r in merged:
        total += (r - l + 1)


    return total


    
print(sol_p2())
