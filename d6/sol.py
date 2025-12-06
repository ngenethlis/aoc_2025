from pprint import pprint
import operator
from functools import reduce


def sol_p1():
    f = open("data.txt", 'r')

    grid = [list(l.split()) for l in f.read().splitlines()]

    pprint(grid)

    n = len(grid)-1
    m = len(grid[0])
    
    ops = {'*' : operator.mul,
           '+' : operator.add}

    sum = 0
    for col in range(m):
        nums = []
        for row in range(n):
            nums.append(int(grid[row][col]))
        op = ops[grid[-1][col]]

        sum += reduce(op, nums)

    return sum



def sol_p2():
    f = open("data.txt", 'r')
    lines = f.readlines()
    grid = list(map(list,zip(*lines)))


    #pprint(grid)

    n = len(grid)
    m = len(grid[0])
    
    ops = {'*' : operator.mul,
           '+' : operator.add}

    sum = 0
    ops_l = []
    nums = []
    for row in range(n):
        cur_n = ''
        for col in range(m):
            elem = grid[row][col]
            if elem not in {' ', '', '\n'}:
                if elem not in ops:
                    cur_n+=elem
                else:
                    ops_l.append(ops[elem])
        nums.append(cur_n)

    probs = []
    curr_prob = []
    for i in range(len(nums)):
        if nums[i] !='':
            curr_prob.append(int(nums[i]))
        if nums[i] == '':
            probs.append(curr_prob)
            curr_prob = []

    #print(ops_l)
    #print(probs)
    
    sum = 0
    for (i,l) in enumerate(probs):
        op = ops_l[i]
        sol = reduce(op, l)
        sum+=sol

    return sum




pprint(sol_p2())

