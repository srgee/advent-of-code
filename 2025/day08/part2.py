
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
    # Parse input data into a list of 3D-coordinates
    boxes = []
    for box in data:
        x, y, z = map(int, box.split(','))
        boxes.append((x, y, z))   
    #print(len(boxes))
    
    # Calculate distance between all possible pairs
    pairs = []
    for i, p in enumerate(boxes):
        for j in range(i+1, len(boxes)):
            # Calculate squared distance for the sake of performance
            q = boxes[j]
            dist = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2
            pairs.append((dist, i, j))  # Store distance and box indices
    #print(len(pairs))

    # Order pairs by distance in ascending order
    pairs.sort(key=lambda x: x[0])

    # Disjoint sets (union-find) are the optimal approach for clustering problems.
    # Use 2 lists: parents (store the parent of each group) and size (store the number of boxes per group)
    # The structure is initialized so that each box is its own parent. To connect boxes you make one the parent and the other the subordinate
    # by adding up its sizes. It is more efficient than using graphs and DFS to find the size for each group. With Union-Find you always know the size of the group
    parents = list(range(len(boxes)))
    sizes = [1] * len(boxes)
    
    def find(i: int) -> int:
        '''Find the parent.'''
        if parents[i] != i:
            parents[i] = find(parents[i])
        return parents[i]


    def union(i: int, j: int) -> bool:
        '''Merge two groups by adding the smallest group to the bigger group.'''
        root_i = find(i)
        root_j = find(j)

        if root_i != root_j:
            if sizes[root_i] < sizes[root_j]:
                parents[root_i] = root_j
                sizes[root_j] += sizes[root_i]
            else:
                parents[root_j] = root_i
                sizes[root_i] += sizes[root_j]
            return True  # Merged groups successfully
        return False  # Groups were already merged

    # Keep connecting boxes untill we get a single circuit
    for _, u, v in pairs:
        union(u, v)
        if max(sizes) == len(boxes):
            return boxes[u][0] * boxes[v][0]    


if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
