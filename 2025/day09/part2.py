from part1 import get_input

def is_valid(p1: tuple[int, int], p2: tuple[int, int], grid: list[list[int]])-> bool:
    tiles = [(x, y) for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1)
                for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1)]
    return all(True if grid[tile[1]][tile[0]] else False for tile in tiles)

def solve(data):
    '''Use DP with tabular states to validate the content of each resulting rectangle.'''
    # 1. Parse input into a binary grid (1 the tile is R or G, 0 forbidden tile)
    # Initializes a X x Y grid with 0, where X is the maximum value of x and Y is the max of y
    reds = [tuple(map(int, coord.split(','))) for coord in data]
    max_x, max_y = 0, 0
    for x, y in reds:
        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y
    grid = [[0] * (max_x + 1)] * (max_y + 1)
    #print(f'Number of columns: {len(grid[0])}, Number of rows: {len(grid)}')
    
    # Draw perimeter
    prev_x, prev_y = None, None
    for i in range(len(reds)):
        x, y = reds[i]
        grid[y][x] = 1
        if x == prev_x:
            step = 1 if y > prev_y else -1
            for j in range(prev_y+step, y, step):
                grid[j][x] = 1
        elif y == prev_y:
            step = 1 if x > prev_x else -1
            for j in range(prev_x+step, x, step):
                grid[y][j] = 1

        prev_x, prev_y = x, y
    else:
        # Close perimeter by connecting first and last tile in the input sequence
        if x == prev_x:
            step = 1 if y > prev_y else -1
            for j in range(prev_y+step, y, step):
                grid[j][x] = 1
        elif y == prev_y:
            step = 1 if x > prev_x else -1
            for j in range(prev_x+step, x, step):
                grid[y][j] = 1

    # Fill in the interior of the polygon with 1s
    for i in range(len(grid)):
        is_inside = False
        for j in range(len(grid[0])):
            if grid[i][j]:
                is_inside = not is_inside
                continue
            if is_inside:
                grid[i][j] = 1

    # 2. Find rectangle of maximum area
    max_area = 0
    for i in range(len(reds)):
        for j in range(i+1, len(reds)):
            if not is_valid(reds[i], reds[j], grid):
                continue
            area = abs(reds[i][0] - reds[j][0] + 1) * abs(reds[i][1] - reds[j][1] + 1)
            if area > max_area:
                #print(f'Local max at {reds[i]}, {reds[j]}')
                max_area = area

    return max_area

def get_largest_area(heights, y, reds):
    stack = []
    local_max = 0
    histogram = heights + [0]
    for x, h in enumerate(histogram):
        while stack and histogram[stack[-1]] >= h:
            height = histogram[stack.pop()]
            width = x if not stack else x - stack[-1] - 1
            left_x = x - width
            right_x = x-1

            # Check if corners are red
            if (left_x, y) in reds and (right_x, y - height + 1) in reds:
                local_max = max(local_max, height * width)
            elif (right_x, y) in reds and (left_x, y - height + 1) in reds:
                local_max = max(local_max, height * width)
    return local_max         


def solve_optimized(data):
    '''
    The problem is solved using coordinate compression to handle massive 
    coordinate ranges without excessive memory consumption. A rectangle is 
    considered valid only if all compressed cells within its boundaries 
    belong to the polygon formed by the sequence of red and green tiles.

    Optimizations:

    1. Coordinate Compression (Space Optimization): Instead of instantiating a matrix for every 
    spatial unit—which would lead to O(width×height) complexity—we map only the critical "event" points
    (the specific X and Y coordinates of the red tiles). This scales down the operational universe 
    to a grid of at most (2N)×(2N).

    2. Orthogonal Scanline Fill (Polygon Filling): We implement a Ray Casting technique specifically
    adapted for grids. By detecting only "vertical walls" (cells with a connection at y-1), we prevent
    the common logic error of flipping the "interior" state while traversing horizontal lines.

    3. Quadratic Candidate Pruning: Since the problem constrains the corners to red tiles,
    the algorithm only needs to evaluate O(N2) pairs of points. When combined with the compressed grid, 
    area integrity validation becomes exceptionally fast, bypassing the need to process billions of empty pixels.

    4. Early Exit Area Check: Before performing the computationally expensive "cell-by-cell" validation
    within the compressed grid, we calculate the mathematical area of the candidate. If this area is
    less than or equal to the current max_area, the candidate is immediately discarded.
    '''
    # 1. Parse input and get limits
    reds = [tuple(map(int, coord.split(','))) for coord in data]
    n = len(reds)
    
    # 2. Coordinates compression
    sorted_x = sorted(list(set([p[0] for p in reds] + [p[0]+1 for p in reds])))
    sorted_y = sorted(list(set([p[1] for p in reds] + [p[1]+1 for p in reds])))
    
    # Maps to find index of real coordinates
    x_map = {val: i for i, val in enumerate(sorted_x)}
    y_map = {val: i for i, val in enumerate(sorted_y)}
    
    # Dimensios of compressed grid
    C, R = len(sorted_x), len(sorted_y)
    grid = [[0] * C for _ in range(R)]

    # 3. Draw perimeter in compressed grid
    for i in range(n):
        p1, p2 = reds[i], reds[(i + 1) % n]
        x1, x2 = sorted( [p1[0], p2[0]] )
        y1, y2 = sorted( [p1[1], p2[1]] )
        
        for iy in range(y_map[y1], y_map[y2] + 1):
            for ix in range(x_map[x1], x_map[x2] + 1):
                grid[iy][ix] = 1 # Perímetro

    # 4. Fill in the interior on the compressed grid
    for iy in range(R):
        inside = False
        for ix in range(C):
            # Usamos la lógica de conexión vertical para el switch
            if grid[iy][ix] == 1:
                if iy > 0 and grid[iy-1][ix] == 1:
                    # Detectar si es un borde vertical real
                    # (Simplificado para polígonos ortogonales)
                    inside = not inside
            elif inside:
                grid[iy][ix] = 1

    # 5. Find largest rectangle with red tile corner check
    # We check all possible red tiles as opposed corners
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = reds[i], reds[j]
            x_min, x_max = sorted([p1[0], p2[0]])
            y_min, y_max = sorted([p1[1], p2[1]])
            
            # El área real
            current_area = (x_max - x_min + 1) * (y_max - y_min + 1)
            if current_area <= max_area:
                continue
            
            # VALIDACIÓN: ¿Todas las celdas comprimidas dentro de este rango son '1'?
            is_valid = True
            for iy in range(y_map[y_min], y_map[y_max]): # Solo hasta el límite de la celda
                for ix in range(x_map[x_min], x_map[x_max]):
                    if grid[iy][ix] == 0:
                        is_valid = False
                        break
                if not is_valid: 
                    break
            
            if is_valid:
                max_area = current_area

    return max_area


if __name__ == '__main__':
    print(f'Sample: {solve_optimized(get_input('sample.txt'))}')
    print(f'Solution: {solve_optimized(get_input('input.txt'))}')
