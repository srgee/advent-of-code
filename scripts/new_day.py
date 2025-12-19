#!/usr/bin/env python3
'''Script to create directory structure and template files for a new AoC's Day.'''
import sys
from pathlib import Path

PART1_TEMPLATE = """
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
    # TODO: implment solution
    pass
    

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
"""

PART2_TEMPLATE = """
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
    # TODO: implment solution
    pass
    

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
"""


def find_next_day(year: int = 2025) -> int:
    '''Find the next day number by looking at existing day directories.'''
    year_path = Path(f'{year}')
    if not year_path.exists():
        return 1
    
    existing_days = []
    for day_path in year_path.glob('day*'):
        if day_path.is_dir():
            try:
                day_num = int(day_path[3:])
                existing_days.append(day_num)
            except ValueError:
                continue

    if not existing_days:
        return 1
    
    return max(existing_days) + 1


def create_day(day: int, year: int = 2025) -> None:
    '''Create new day's directory structure.'''
    day_path = Path(f'{year}/day{day:02d}')
    day_path.mkdir(parents=True, exist_ok=True)

    (day_path / '__init__.py').write_text('')
    (day_path / 'part1.py').write_text(PART1_TEMPLATE)
    (day_path / 'part2.py').write_text(PART2_TEMPLATE)

    print(f'Created structure for day {day:02d} at {day_path}')
    print('\nNext steps:')
    print(f'1. Visit https://adventofcode.com/{year}/day/{day}')
    print(f"2. Copy sample input to {day_path}/sample.txt")
    print(f"3. Copy your puzzle input to {day_path}/input.txt")
    print("4. Start coding!!!!")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit('Usage: python scripts/new_day.py [day_number]')

    if len(sys.argv) == 2:
        try:
            day = int(sys.argv[1])
            if not 1 <= day <= 25:
                sys.exit('Argument day_number must ba a number between 1 and 25 both inclusive')
        except ValueError:
            sys.exit('Argument day_number must be a valid day number')
    else:
        # Auto-detect next day
        day = find_next_day()
        if day > 25:
            sys.exist('All 25 days already exist!')
        print(f'Detected day {day} automagically')

    create_day(day)