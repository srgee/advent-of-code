
from pathlib import Path

def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def solve(data: list[str]) -> int:
    sep_index = data.index('')

    # Parse fresh ranges. NOTE: python ranges are not both-inclusive so we need to add 1 to upper bound
    fresh_ranges = []
    for i in range(sep_index):
        range_limits = data[i].split('-')
        fresh_ranges.append(range(int(range_limits[0]), int(range_limits[1])+1))
    #print(f'Parsing fresh ranges: {fresh_ranges}')

    # Parse available ingredients
    ingredients = [int(data[i]) for i in range(sep_index+1, len(data))]
    #print(f'Available ingredientes: {ingredients}')

    # Count available fresh ingredients
    count = 0
    for id in ingredients:
        if any(id in r for r in fresh_ranges):
            count += 1

    return count
    
if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
