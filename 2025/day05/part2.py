from part1 import get_input


def solve(data):
    '''Part1 solution based on range objects does not scale (execution got aborted). Use list of lists and a merge interval algorithm instead.'''
    sep_index = data.index('')

    # Parse first part of the database as list of lists [start, end]
    fresh_ranges = []
    for i in range(sep_index):
        start, end = map(int, data[i].split('-'))
        fresh_ranges.append([start, end])
    fresh_ranges.sort()
    
    merged = [fresh_ranges[0]]
    for current in fresh_ranges[1:]:
        _, prev_end = merged[-1]
        curr_start, curr_end = current
        
        # Check overlap
        if curr_start <= prev_end:
            # FMerge extending at the end of the list if necessary
            merged[-1][1] = max(prev_end, curr_end)
        else:
            # Add new interval
            merged.append(current)


    return sum(end - start + 1 for start, end in merged)

if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
