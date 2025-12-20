from pathlib import Path
import math


def get_input(filename: str) -> str:    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        return f.readlines()

def solve(data: list[str]) -> int:
    # Parse operands into a list of list. The inner list are the operands per problem and the outer list contains the problems.
    num_cols = len(data[0]) # Max number of columns including \n
    num_rows = len(data)
    operands, problems = [], []
    for i in range(num_cols-1):
        number = [data[n][-2-i] for n in range(num_rows-1) if data[n][-2-i] != ' ']
        if not number:
            problems.append(operands)
            operands = []
            continue
        operands.append(int(''.join(number)))
    else:
        problems.append(operands)
    #print(problems)

    # Parse operators
    operators = data[-1].split()
    #print(operators)

    # Do the math
    totals = []
    for operation, numbers in zip(reversed(operators), problems):
        #print(operation, numbers)
        if operation == '+':
            totals.append(sum(numbers))
        elif operation == '*':
            totals.append(math.prod(numbers))
    
    return sum(totals)


    """     accumulated = 0
        step = num_rows - 1
        #print(step)
        start, stop = 0, step
        for i in range(len(operators)):
            #print(start, stop)
            if operators[-1-i] == '*':
                result = math.prod(operands[start:stop])
            elif operators[-1-i] == '+':
                result = sum(operands[start:stop])
            else:
                result = 0
            accumulated += result
            start, stop = stop, stop + step
    """

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
