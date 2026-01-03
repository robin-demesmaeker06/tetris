# settings.py

# Game Area
CELL_SIZE = 40
COLS = 10
ROWS = 22
GAME_WIDTH = CELL_SIZE * COLS  # The Tetris Grid width
SIDEBAR_WIDTH = 200            # New Sidebar area
WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
HEIGHT = CELL_SIZE * ROWS

# --- COLORS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)

# Tetris Colors
CYAN = (0, 255, 255)    # I
BLUE = (0, 0, 255)      # J
ORANGE = (255, 165, 0)  # L
YELLOW = (255, 255, 0)  # O
GREEN = (0, 255, 0)     # S
PURPLE = (128, 0, 128)  # T
RED = (255, 0, 0)       # Z

# --- SHAPES DICTIONARY ---
# Format: { 'Key': [List of (x, y) coordinates] }
SHAPES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
    'J': [(0, 0), (-1, 0), (-1, -1), (1, 0)],
    'L': [(0, 0), (1, 0), (1, -1), (-1, 0)],
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)]
}

# --- COLOR MAP ---
# This maps the shape key to a color
SHAPE_COLORS = {
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE,
    'I': CYAN,
    'O': YELLOW
}

# settings.py

# Key = Level, Value = Milliseconds (lower is faster)
LEVEL_SPEEDS = {
    1: 500,  # 0.5 seconds (Start)
    2: 400,
    3: 300,
    4: 200,
    5: 150,  # Super fast!
}