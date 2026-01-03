# utils.py
import random
from settings import *

def rotate_shape(shape, shape_type):
    # The 'O' piece (Square) should never rotate!
    if shape_type == 'O':
        return shape

    # For everything else, apply the math
    new_shape = []
    for block in shape:
        x, y = block
        new_x = y * -1
        new_y = x
        new_shape.append((new_x, new_y))
    return new_shape

def check_collision(board, shape, offset_x, offset_y):
    for block in shape:
        dx, dy = block
        x = offset_x + dx
        y = offset_y + dy
        
        # 1. Wall Checks
        if x < 0 or x >= COLS or y >= ROWS:
            return True
            
        # 2. Board Checks (The Stacking Fix!)
        # We only check the board if y is positive (on screen)
        if y >= 0:
            if board[y][x] != BLACK:
                return True
                
    return False

def clear_rows(board):
    # 1. Filter: Keep only rows that have at least one BLACK cell
    # (i.e., rows that are NOT full)
    new_board = [row for row in board if BLACK in row]
    
    # 2. Calculate how many lines were removed
    lines_cleared = ROWS - len(new_board)
    
    # 3. Refill: Add fresh empty rows to the top
    for _ in range(lines_cleared):
        new_board.insert(0, [BLACK for _ in range(COLS)])
        
    return new_board, lines_cleared

def get_random_piece():
    key = random.choice(list(SHAPES.keys()))
    return key, SHAPES[key], SHAPE_COLORS[key]