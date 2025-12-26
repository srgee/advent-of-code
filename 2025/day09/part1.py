
from pathlib import Path

def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def solve(data):
    # Parse input data into a list of tuples (col, row)
    reds = [tuple(map(int, coord.split(','))) for coord in data]
    print(f'Input size: {len(reds)}')

    # Find max area by brute force (all combinations)
    max_area = 0
    for i in range(len(reds)):
        for j in range(i+1, len(reds)):
            area = abs(reds[i][0] - reds[j][0] + 1) * abs(reds[i][1] - reds[j][1] + 1)
            if area > max_area:
                #print(f'Local max at {reds[i]}, {reds[j]}')
                max_area = area

    return max_area
    

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
