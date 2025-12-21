
from pathlib import Path

from collections import deque, namedtuple

def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def solve(data: list[str]) -> int:
    '''Implement BFS algorithm usinf a doble-ended queue and a set for explored cells. Whenever we hit a splitter we increment count and and split the beam.'''
    Point = namedtuple('Point', 'row col')

    # Parse input data into a list of splitter coordinates (row, col)
    splitter_coords = []
    max_row, max_col = len(data), len(data[0])
    for i in range(max_row):
        for j in range(max_col):
            if data[i][j] == '^':
                splitter_coords.append(Point(i, j))
    
    start = Point(0, data[0].find('S'))
    splits = 0
    explored = set()
    explored.add(start)
    queue = deque()
    queue.append(start)
    while queue:
        current = queue.popleft()
        if current in splitter_coords:
            splits += 1

            # Split
            for dcol in (-1, 1):
                adjacent = Point(current.row, current.col+dcol)
                if adjacent.row < max_row and adjacent.col < max_col and adjacent not in explored:
                    queue.append(adjacent)
                    explored.add(adjacent)
        else:
            # Move down
            adjacent = Point(current.row+1, current.col)
            if adjacent.row < max_row and adjacent.col < max_col and adjacent not in explored:
                queue.append(adjacent)
                explored.add(adjacent)

    return splits

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
