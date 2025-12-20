from pathlib import Path
import math

def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.split())
    
    return input_lines

def solve(data: list[str]) -> int:
    max_row, max_col = len(data), len(data[0])
    accumulated = 0
    for col in range(max_col):
        *operands, operator = [int(data[i][col]) if i < max_row-1 else data[i][col] for i in range(max_row)]
        #print(f'Column {col}: {operands} | Operator: {operator}')
        if operator == '*':
            result = math.prod(operands)
        elif operator == '+':
            result = sum(operands)
        else:
            result = 0
        accumulated += result
    
    return accumulated


if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
