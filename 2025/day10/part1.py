import itertools
import re
from pathlib import Path


def get_input(filename: str) -> str:
    '''Read input file and returns a list of text clean lines (removes end of line characters).'''
    file_path = Path(__file__).parent / filename
    with file_path.open() as f:
        input_lines = []
        while line := f.readline():
            input_lines.append(line.strip())
    
    return input_lines


def solve(input_data):
    '''
    Each button functions as a XOR operation. Pressing a button once toggles
    the state of the indicator lights; pressing it a second time reverts
    them to their original state. Consequently, to find the minimum number
    of presses, there are only two possible states for each button (either press it once,
    or not press it).
    
    Any odd number of presses is logically equivalent to pressing the button once,
    while any even number of presses (2, 4, 6, etc.) is equivalent to zero presses.
    
    Use bitmask to represent lights as bits and binary XOR operations to toggle lights.
    Since there are a "small" number of buttons per machine (2^N combinations 
    where N < 15) we can afford to explore combinations of buttons.

    To guarantee minimum number of clicks we start exploring combinations
    incrementally: 0, 1, 2, etc. As soon as we hit the target mask, we stop exploration.
    '''
    total_presses = 0
    for line in input_data:
        # Extract light diagrams [square brackets]
        diagram_match = re.search(r'\[([.#]+)\]', line)
        diagram_str = diagram_match.group(1)
        
        # Create target bitmask
        target_mask = 0
        for i, char in enumerate(diagram_str):
            if char == '#':
                target_mask |= (1 << i)
        
        # Extract buttons (parentheses)
        button_matches = re.findall(r'\(([\d,]+)\)', line)
        button_masks = []
        for btn_str in button_matches:
            indices = map(int, btn_str.split(','))
            mask = 0
            for idx in indices:
                mask |= (1 << idx)
            button_masks.append(mask)
            
        # Find minimum number of button presses
        found = False
        num_buttons = len(button_masks)
        
        for r in range(num_buttons + 1):
            for combo in itertools.combinations(button_masks, r):
                current_state = 0
                for btn_mask in combo:
                    current_state ^= btn_mask   # Binary XOR (toggle lights)
                
                if current_state == target_mask:
                    total_presses += r
                    found = True
                    break
            if found:
                break
                
    return total_presses


if __name__ == '__main__':
    print(f'Sample: {solve(get_input('sample.txt'))}')
    print(f'Solution: {solve(get_input('input.txt'))}')
