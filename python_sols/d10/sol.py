## File format
## each line  [] (d(, d)*)+ {d(,d)*}
## [(.*|#*)*] indicator lights where . OFF , # ONa
## (d (,d)*) button whiring schematics
## {} joltage reqs

## Machine has number of indicators shown all OFF
## To turn machine on must match its indicator lights to diagram
## Each button indicates which light(s) it toggles, i.e (0) toggles 0
## (1,2,3) toggles lights 1 2 and 3

## Only integer pushes of buttons

## Ignore joltage for p1


## Find fewest num of presses to config all lights


import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


lights_re = "[.#]+"
buttons_re = "(\d[,\d]*)"
joltage_re = "{\d[,\d]*}"

from collections import deque

def solve_bfs(target_val, num_lights, buttons):
    # start state is all 0's
    # queue stores curr state, press cnt
    queue = deque([(0, 0)])

    visited = {0}

    while queue:
        current_state, presses = queue.popleft()

        if current_state == target_val:
            return presses

        for btn_mask in buttons:
            # XOR to toggle lights
            next_state = current_state ^ btn_mask

            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, presses + 1))

    return 0

def find_min_presses(line : str):
    lights_match = re.search(r"\[([.#]+)\]", line)
    raw_lights = lights_match.group(1)
    num_lights = len(raw_lights)

    # Convert target pattern to integer (bitmask)
    target = 0
    for i, char in enumerate(raw_lights):
        if char == '#':
            target |= (1 << i)

    # conv buttons to bitmask
    raw_buttons = re.findall(r"\(([\d,]+)\)", line)
    button_masks = []

    for b_str in raw_buttons:
        indices = map(int, b_str.split(','))
        b_mask = 0
        for idx in indices:
            b_mask |= (1 << idx)
        button_masks.append(b_mask)

    return solve_bfs(target, num_lights, button_masks)


def sol_p1():
    f = open("data.txt", 'r')
    presses = 0
    for l in f.readlines():
        presses += find_min_presses(l.strip())

    print(presses)



## P2 ignore lights, care about joltage


## Machine has number of joltage counters start at 0's
## Must match joltage counters to actual ones
## Each button indicates which counters it increments (by 1)
## (1,3) does jolt[1]++, jolt[3]++
## fewer presses to get to req joltage
## Solving Ax=b where
# A columns are buttons
# x is how many times we press each button
# b is target joltage vector
# so we need to do x = A^-1b
def solve_machine_milp(line):
    raw_targets = re.search(r"\{([\d,]+)\}", line).group(1)
    b = np.array([int(x) for x in raw_targets.split(',')], dtype=float)

    # construct matrix A
    # Each button represents a COLUMN in the matrix A.
    # If a button affects counter i, then A[i][column] = 1.
    raw_buttons = re.findall(r"\(([\d,]+)\)", line)

    num_rows = len(b)
    num_cols = len(raw_buttons)

    A = np.zeros((num_rows, num_cols))

    for col_idx, btn_str in enumerate(raw_buttons):
        indices = map(int, btn_str.split(','))
        for row_idx in indices:
            if row_idx < num_rows:
                A[row_idx, col_idx] = 1


    # Minimize sum of x. (c vector is all 1s)
    c = np.ones(num_cols)

    # Constraint: Ax = b
    # For equality, we set lb = ub = b
    constraint = LinearConstraint(A, lb=b, ub=b)

    # Bounds: x >= 0 (You can't press a button negative times)
    bounds = Bounds(lb=0, ub=np.inf)

    # Integrality: 1 means the variable must be an integer.
    integrality = np.ones(num_cols) 

    res = milp(c=c, constraints=constraint, bounds=bounds, integrality=integrality)

    if res.success:
        return int(np.round(np.sum(res.x)))
    else:
        return 0

def sol_p2():


    with open("data.txt", 'r') as f:
        lines = f.readlines()

    total_presses = 0


    for line in lines:
        if not line.strip(): continue

        targets = re.search(r"\{([\d,]+)\}", line).group(1)

        min_p = solve_machine_milp(line)

        print(f"Joltage {{{targets}}} | {min_p}")
        total_presses += min_p

    return total_presses

print(sol_p2())
