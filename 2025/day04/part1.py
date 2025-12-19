
from pathlib import Path


def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def parse_input(data: list[str]) -> list[(int, int)]:
    '''Return a list of coordinates (row, col) for paper rolls.'''
    coordinates = []
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == '@':
                #print(f'{item} en coordenadas ({i, j})')
                coordinates.append((i, j))
    
    return coordinates 


def get_adjacents(row: int, col:int, dim: int) -> list[(int, int)]:
    '''Return list of adjacents to the given point of a dim x dim grid.'''
    adjacents = []
    for i in range(-1, 2):
        for j in range (-1, 2):
            if (i == 0) & (j == 0):
                continue
            new_row = row + i
            new_col = col + j
            if (0 <= new_row < dim) & (0 <= new_col < dim):
                adjacents.append((new_row, new_col))

    return adjacents


def solve(data: str) -> int:
    accessibles = 0
    rolls_coordinates = parse_input(data)
    #print(rolls_coordinates)
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item != '@':
                continue
            adjacents = get_adjacents(i, j, len(row))
            #print(f'{len(adjacents)} adjacent positions to position {i, j}')
            adjacent_rolls = [pos for pos in adjacents if pos in rolls_coordinates]
            if len(adjacent_rolls) < 4:
                accessibles += 1

    return accessibles 
            

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
