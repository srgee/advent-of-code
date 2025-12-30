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
    # Parse input data into a graph: devices are nodes and edges are connections.
    adjacents = dict()
    for line in data:
        device, connections = line.split(':')
        adjacents[device] = [c for c in connections.split(' ') if len(c) > 1]
    #print(adjacents)

    # Implement DFS to explore all paths
    paths = 0
    devices = ['you']
    #visited = set()
    while devices:
        device = devices.pop()      # Remove last item (LIFO)
        #if device in visited:
        #    continue

       #visited.add(device)
        if adjacents[device] == ['out']:
            paths += 1
        else:
            # Add adjacent devices to explore further. Keep same order as in the adjacents list
            devices.extend(reversed(adjacents[device]))

    return paths


if __name__ == '__main__':
    #print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
