# main.py
import pygame
import random

from settings import *
from utils import *

# main.py

pygame.init()
pygame.mixer.init()  # <--- Initialize the sound system

# --- LOAD SOUNDS ---
try:
    # 1. Background Music (Streamed)
    pygame.mixer.music.load('assets/sounds/music.mp3')
    pygame.mixer.music.set_volume(0.3)  # 30% volume so it's not too loud
    pygame.mixer.music.play(-1)         # Play infinitely (-1 loop)

    # 2. Sound Effects
    rotate_sfx = pygame.mixer.Sound('assets/sounds/rotate.wav')
    clear_sfx = pygame.mixer.Sound('assets/sounds/clear.wav')
    drop_sfx = pygame.mixer.Sound('assets/sounds/drop.wav')
    levelup_sfx = pygame.mixer.Sound('assets/sounds/levelup.wav')

    # Adjust volumes if needed
    rotate_sfx.set_volume(0.5)
    clear_sfx.set_volume(0.5)
    drop_sfx.set_volume(0.8) # Keep the explosion loud!

except Exception as e:
    print(f"Warning: Sound failed to load. {e}")
    # Dummy class to prevent crashing if files are missing
    class DummySound:
        def play(self): pass
    rotate_sfx = clear_sfx = drop_sfx = DummySound()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- STATE VARIABLES ---
game_board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

current_key, current_shape, current_color = get_random_piece()
next_key, next_shape, next_color = get_random_piece()

grid_x = 5
grid_y = 0

fall_timer = 0
fall_speed = 30

score = 0
total_lines = 0     # <--- Add this
level = 1           # <--- Add this

running = True
game_over = False
while running:
    
    # 1. INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_over:
                # --- GAME OVER CONTROLS ---
            if event.key == pygame.K_SPACE:
                # RESET THE GAME
                game_board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
                score = 0
                game_over = False
                # (You might need to reset current_shape here too)
            if event.key == pygame.K_ESCAPE:
                running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(game_board, current_shape, grid_x - 1, grid_y):
                        grid_x -= 1
                if event.key == pygame.K_RIGHT:
                    if not check_collision(game_board, current_shape, grid_x + 1, grid_y):
                        grid_x += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(game_board, current_shape, grid_x, grid_y + 1):
                        grid_y += 1
                if event.key == pygame.K_UP:
                    rotated = rotate_shape(current_shape, current_key)
                    if not check_collision(game_board, rotated, grid_x, grid_y):
                        current_shape = rotated
                        rotate_sfx.play()
                        # SPACE: Hard Drop (Instant fall)
                if event.key == pygame.K_SPACE:
                    # 1. Move down until we hit something
                    while not check_collision(game_board, current_shape, grid_x, grid_y + 1):
                        grid_y += 1
                    
                    # 2. Force the timer to trigger the lock immediately
                    fall_timer = fall_speed
                    drop_sfx.play()

    # 2. UPDATE
    if not game_over:
        fall_timer += 1
        if fall_timer >= fall_speed:
            if not check_collision(game_board, current_shape, grid_x, grid_y + 1):
                grid_y += 1
                fall_timer = 0
            else:
                # Lock the piece
                for block in current_shape:
                    x = grid_x + block[0]
                    y = grid_y + block[1]
                    if 0 <= y < ROWS and 0 <= x < COLS:
                        game_board[y][x] = current_color
                
                # We send the dirty board to utils, and get back a clean one + the score
                game_board, lines_cleared = clear_rows(game_board)
                
                # --- UPDATE SCORE & LEVEL ---
                if lines_cleared > 0:
                    clear_sfx.play()  # Play the normal clear sound
                    
                    # 1. Remember the OLD level before updating
                    old_level = level
                    
                    # 2. Update totals
                    total_lines += lines_cleared
                    
                    # 3. Calculate NEW level
                    level = (total_lines // 10) + 1
                    if level > 5: level = 5
                    
                    # 4. Check for Level Up
                    if level > old_level:
                        levelup_sfx.play() # <--- PLAY THE NEW SOUND
                        print(f"Level Up! Now at Level {level}")
                    
                    # Update speed
                    fall_speed = LEVEL_SPEEDS[level] // 16
                    
                    # Score calculation
                    match lines_cleared:
                        case 1: score += 100
                        case 2: score += 300
                        case 3: score += 500
                        case 4: score += 1200
                
                # SPAWN NEW PIECE
                # 1. Promote Next to Current
                current_key, current_shape, current_color = next_key, next_shape, next_color
                
                # 2. Generate a brand new Next
                next_key, next_shape, next_color = get_random_piece()
                
                grid_x = 5
                grid_y = 0
                fall_timer = 0

                # Check if the new piece is already hitting something at the spawn point
                if check_collision(game_board, current_shape, grid_x, grid_y):
                    print("GAME OVER!")
                    game_over = True
                    pygame.mixer.music.stop()

    # 3. RENDER
    screen.fill(BLACK) # Clear screen

    # --- DRAW SIDEBAR BACKGROUND ---
    sidebar_rect = pygame.Rect(GAME_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, (30, 30, 30), sidebar_rect) # Dark Grey Sidebar

    # --- DRAW BOARD (Same as before) ---
    for y in range(ROWS):
        for x in range(COLS):
            if game_board[y][x] != BLACK:
                pygame.draw.rect(screen, game_board[y][x], 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # ---------------------------------------
    # 1. DRAW GHOST PIECE (The Shadow)
    # ---------------------------------------
    ghost_y = grid_y
    # Calculate where it lands
    while not check_collision(game_board, current_shape, grid_x, ghost_y + 1):
        ghost_y += 1

    # Draw the grey outline
    for block in current_shape:
        x = (grid_x + block[0]) * CELL_SIZE
        y = (ghost_y + block[1]) * CELL_SIZE
        pygame.draw.rect(screen, GREY, (x, y, CELL_SIZE, CELL_SIZE), 2)

    # ---------------------------------------
    # 2. DRAW CURRENT PIECE (The Real Block)
    # ---------------------------------------
    # This loop was likely deleted! Put it back:
    for block in current_shape:  # <--- CHECK THIS LOOP
        x = (grid_x + block[0]) * CELL_SIZE
        y = (grid_y + block[1]) * CELL_SIZE
        pygame.draw.rect(screen, current_color, (x, y, CELL_SIZE, CELL_SIZE))

    # --- DRAW GRID LINES (Only on the game board!) ---
    for x in range(COLS + 1): # +1 to draw the rightmost border
        pygame.draw.line(screen, GREY, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(screen, GREY, (0, y * CELL_SIZE), (GAME_WIDTH, y * CELL_SIZE))

    # --- DRAW UI (Score & Next Piece) ---
    # 1. Score
    score_label = font.render("SCORE", True, WHITE)
    score_value = font.render(str(score), True, WHITE)
    screen.blit(score_label, (GAME_WIDTH + 20, 20))
    screen.blit(score_value, (GAME_WIDTH + 20, 50))

    # 1.2 Level
    level_label = font.render("LEVEL", True, WHITE)
    level_value = font.render(str(level), True, WHITE)
    screen.blit(level_label, (GAME_WIDTH + 20, 80)) # Slightly below score
    screen.blit(level_value, (GAME_WIDTH + 20, 105))

    # 2. Next Piece Label
    next_label = font.render("NEXT", True, WHITE)
    screen.blit(next_label, (GAME_WIDTH + 20, 135))

    # 3. Draw the "Next Piece" preview
    # We draw it at a fixed offset in the sidebar (e.g., x=GAME_WIDTH + 50, y=150)
    preview_x = GAME_WIDTH + 70
    preview_y = 225
    
    # Example for drawing the NEXT piece with borders
    for block in next_shape:
        px = preview_x + (block[0] * CELL_SIZE)
        py = preview_y + (block[1] * CELL_SIZE)
        
        # 1. Draw the filled color
        pygame.draw.rect(screen, next_color, (px, py, CELL_SIZE, CELL_SIZE))
        
        # 2. Draw a Black Border (width = 1 or 2)
        pygame.draw.rect(screen, BLACK, (px, py, CELL_SIZE, CELL_SIZE), 1) # <--- NEW

    # (Add your Game Over overlay here)

    if game_over:
        # Create a semi-transparent overlay
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(128) # Transparency (0-255)
        s.fill((0, 0, 0)) # Black
        screen.blit(s, (0, 0))
        
        # Draw Text
        over_text = font.render("GAME OVER", True, WHITE)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        
        # Center the text
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()