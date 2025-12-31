from part1 import get_input

def solve_sample(data):
    # Parse input data into an adjacent list (dict)
    adjacents = dict()
    for line in data:
        device, connections = line.split(':')
        adjacents[device] = [c for c in connections.split(' ') if len(c) > 1]
    #print(adjacents)

    paths = 0
    
    def find_paths(current: str, visited: set[str], has_dac: bool, has_fft: bool) -> None:
        '''Implement recursive backtracking.'''
        nonlocal paths
        
        # Base case: hit target device "out"
        if current == 'out':
            if has_dac and has_fft:
                paths += 1
            return

        # Recursive case: explore adjacents of current device
        for adjacent in adjacents.get(current, []):
            if adjacent not in visited:
                visited.add(adjacent)

                find_paths(
                    adjacent, 
                    visited,
                    has_dac or adjacent == 'dac',
                    has_fft or adjacent == 'fft'
                )
                
                # Backtrack: undo for other routes
                visited.remove(adjacent)

    find_paths('svr', {'svr'}, has_dac=False, has_fft=False)

    return paths


def solve(data):
    '''
    Initial solution was DFS with recursive backtracking. It worked for the sample data.
    It breaks for the input.txt because the graph has many nodes and there are nodes
    with many connections --> combinatorial explosion

    Divide and conquer: instead of traversing all paths we will count valid paths. A path
    is valid when either one of the following sequence of events happen:

    1. The route visits "fft" and then "dac"
    2. the rout visits "dac" and then "fft"

    Since the input is a DAG we can count valid paths between 2 nodes almost instantly
    using a cache (memo).
    '''
    # Parse input data into an adjacent list (dict)
    adjacents = dict()
    for line in data:
        device, connections = line.split(':')
        adjacents[device] = [c for c in connections.split(' ') if len(c) > 1]
    #print(adjacents)

    # Initializes cache
    memo = dict()

    def count_paths(u: str, target: str) -> int:
        '''Count paths between two nodes recursively.'''
        # Base case
        if u == target:
            return 1
        if (u, target) in memo:
            return memo[(u, target)]
        
        # Recursive case
        total = 0
        for v in adjacents.get(u, []):
            total += count_paths(v, target)
        
        memo[(u, target)] = total
        return total

    # Count valid paths for the sequence:
    # SVR -> FFT -> DAC -> OUT
    path_svr_fft = count_paths('svr', 'fft')
    path_fft_dac = count_paths('fft', 'dac')
    path_dac_out = count_paths('dac', 'out')
    
    total_seq1 = path_svr_fft * path_fft_dac * path_dac_out

    # Count paths for: SVR -> DAC -> FFT -> OUT
    memo.clear()
    path_svr_dac = count_paths('svr', 'dac')
    path_dac_fft = count_paths('dac', 'fft')
    path_fft_out = count_paths('fft', 'out')

    total_seq2 = path_svr_dac * path_dac_fft * path_fft_out

    return total_seq1 + total_seq2


if __name__ == '__main__':
    sample = '''
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
    '''
    #print(f'Sample: {solve_sample(sample.strip().splitlines())}')
    print(f'Solution: {solve(get_input('input.txt'))}')
