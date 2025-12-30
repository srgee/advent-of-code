from part1 import get_input
import re
from scipy.optimize import linprog
import numpy as np
from tqdm import tqdm


def solve_machine(data: str) -> int:
    # Parse buttons
    buttons = re.findall(r'\(([\d,]+)\)', data)
    raw_joltages = re.search(r'\{([\d,]+)\}', data).group(1)
    counters = [int(j) for j in raw_joltages.split(',')]

    # Build coeficients matrix A (counters x buttons)
    coefficients = np.zeros((len(counters), len(buttons)), dtype=np.uint16)
    for b_idx, b_str in enumerate(buttons):
        affected_counters = [int(c) for c in b_str.split(',')]
        for c_idx in affected_counters:
            coefficients[c_idx, b_idx] = 1
    
    # Optimization: the function linprog can minimize a linear objective function
    # subject to linear equality and inequality constraints
    obj_coeffs = np.ones(len(buttons))  # Coeficients of objective function

    # Equality constraint: A * X = counters
    # Inequality constraint: xi >= 0
    res = linprog(obj_coeffs, A_eq=coefficients, b_eq=counters, bounds=(0, None), method='highs')

    """ 
        print(f'Buttons: {buttons}')
        print(f'counters: {counters}')
        print(f'=========== RESULT: {int(np.round(res.x).sum()) if res.success else 0}')
        while input():
            break
    """

    # Result must be an integer so we round the solution
    return int(np.round(res.x).sum()) if res.success else 0


def solve(data):
    '''# TODO: implement solution
    Now every button press counts, so the number of combinations is unmanageable.
    This is a Linear Algebra optimization problem. Each button is a variable xi
    (press counter) and every joltage requirements is an equation. 

    Example:
    For these requirements {3,5,4,7} with buttons (3), (1,3), (2), (2,3), (0,2), (0,1)
    we have the following system of linear equations:

    Counter 0: x4 + x5 = 3

    Counter 1:  x1 + x5 = 5

    Counter 2:  x2 + x3 + x4 = 4

    Counter 3: x0 + x1 + x3 = 7

    Where xi >= 0 (integer)

    We want to minimize  Z = x0 + x1 + x2 + x3 + x4 + x5

    Use Lineal Programming to solve the system: A * X = Y where rows are counters
    and columns are buttons. 
    '''
    clicks = 0
    for line in tqdm(data):
        clicks += solve_machine(line)

    return clicks


if __name__ == '__main__':
    #print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
