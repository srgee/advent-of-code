from part1 import get_input
from collections import namedtuple
from functools import cache




def solve(data):
    '''
    Uses a recursive DFS algorithm with memoization.
    
    Since the beams always move down, there are no loops. The recursive function answers this: 
    “If I am at this point, how many completed timelines will result?”

    Base Case: If I’m off the grid, I’ve finished one valid timeline. Return 1.
    Recursive Step:
        If I’m at a ^: result is count_timelines(left) + count_timelines(right).
        Otherwise: result is count_timelines(down).

    '''
    Point = namedtuple('Point', 'row col')
    start = Point(0, data[0].find('S'))
    max_row, max_col = len(data) - 1, len(data[0]) - 1

    @cache
    def count_timelines(point:Point) -> int:
        '''Recursive DFS to count timelines that result from a particle at "point".'''
        if point.row > max_row or point.col > max_col:
            # The particle has exited the manifold. It counts as a valid timeline.
            return 1
        
        if data[point.row][point.col] == '^':
            # Split. Both new timelines continue downward.
            left = Point(point.row+1, point.col-1)
            right = Point(point.row+1, point.col+1)
            return count_timelines(left) + count_timelines(right)
        else:
            # Continue downward
            return count_timelines(Point(point.row+1, point.col))

    return count_timelines(start)
  

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
