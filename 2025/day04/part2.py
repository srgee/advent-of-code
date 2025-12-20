from part1 import get_input


def parse_input(data: list[str]) -> set[tuple[int, int]]:
    '''Return a set of coordinates (row, col) for paper rolls in input data.'''
    coordinates = set()
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == '@':
                #print(f'{item} en coordenadas ({i, j})')
                coordinates.add((i, j))
    
    return coordinates 


def get_adjacents(row:int, col:int, dim: int) -> set[tuple[int, int]]:
    ''''Return a set of coordinates (tuples) of adjacents of teh given cell. It assumes a dim x dim grid.'''
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
    
def get_removable_rolls(data, rolls):
    removable = set()
    for i in range(len(data)):
        for j in range(len(data)):
            if (i, j) not in rolls:
                continue
            
            if len(rolls & get_adjacents(i, j, len(data))) < 4:
                removable.add((i, j))

    return removable


def solve(data: list[str]) -> int:
    accummulated = 0
    rolls = parse_input(data)
    while removable_rolls := get_removable_rolls(data, rolls):
        accummulated += len(removable_rolls)
        rolls -= removable_rolls
    
    return accummulated
    

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Sample: {solve(get_input('input.txt'))}')