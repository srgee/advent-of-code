
from pathlib import Path


def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def parse_input(data: list[str]) -> set[tuple[int, int]]:
    '''Return a set of coordinates (row, col) for paper rolls.'''
    coordinates = set()
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == '@':
                #print(f'{item} en coordenadas ({i, j})')
                coordinates.add((i, j))
    
    return coordinates 


def get_adjacents(row: int, col: int, dim: int) -> set[tuple[int, int]]:
    '''Return set of adjacent cells to the given cell in a dim x dim grid.'''
    adjacents = set()
    for i in range(-1, 2):
        for j in range (-1, 2):
            if (i == 0) & (j == 0):
                continue
            new_row = row + i
            new_col = col + j
            if (0 <= new_row < dim) & (0 <= new_col < dim):
                adjacents.add((new_row, new_col))

    return adjacents


def solve(data: list[str]) -> int:
    accessibles = 0
    rolls = parse_input(data)
    for i in range(len(data)):
        for j in range(len(data)):
            if (i, j) not in rolls:
                continue

            if len(rolls & get_adjacents(i, j, len(data))) < 4:
                accessibles += 1
    
    return accessibles

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
