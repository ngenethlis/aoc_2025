## Format
## List of present <index>: \n shape
## shape : # part, . is not newlines for more than one line shape
## Second section : tree regions
## ^ <width>x<length>: (\d )*
## so 1 0 1 0 3 2:
# 1 id 0, 0 id 1, 1 id 2, ... 2 id 5
# pres[id]=#presents with that id

## can flip and rotate shapes

from collections import defaultdict

## actual input file doesn't have interlocking shapes lol
def fits(dims, pres, shape_areas):
    w, l = map(int, dims.split('x'))
    avail_area = w * l

    pres = list(map(int, pres.split()))

    area_taken = sum(cnt * shape_areas[i] for (i, cnt) in enumerate(pres))

    return 1 if area_taken <= avail_area else 0

def sol_p1():
    lines = open("data.txt").readlines() 
    shape_areas = defaultdict(int)
    cur_id = -1
    res = 0

    for line in lines:
        line = line.strip()
        if 'x' in line:
            dim, presents = line.split(':')
            res += fits(dim, presents, shape_areas) 
        elif ':' in line:
            cur_id = int(line[:-1])
            shape_areas[cur_id] = 0 

        elif '#' in line:
            shape_areas[cur_id] += line.count('#')

    print(res)

sol_p1()
