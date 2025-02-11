import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY  = (180, 180, 180)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Board dimensions (Connect Four standard)
COLUMNS = 7  # number of columns (horizontal)
ROWS    = 6  # number of rows (vertical)

# Drawing settings
SQUARE_SIZE   = 100
WIDTH         = COLUMNS * SQUARE_SIZE  # 7 * 100 = 700
HEIGHT        = ROWS * SQUARE_SIZE     # 6 * 100 = 600
LINE_WIDTH    = 5
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH  = 15
CROSS_WIDTH   = 25

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect 4')
screen.fill(BLACK)

# Initialize board (a 6 x 7 array filled with zeros)
board = np.zeros((ROWS, COLUMNS))

def draw_lines(color=WHITE):
    # Draw vertical lines
    for c in range(1, COLUMNS):
        pygame.draw.line(screen, color, (c * SQUARE_SIZE, 0), (c * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # Draw horizontal lines
    for r in range(1, ROWS):
        pygame.draw.line(screen, color, (0, r * SQUARE_SIZE), (WIDTH, r * SQUARE_SIZE), LINE_WIDTH)

def draw_figures(color=WHITE):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == 1:
                # Draw player 1 piece (circle)
                pygame.draw.circle(screen, color,
                                   (int(c * SQUARE_SIZE + SQUARE_SIZE/2), int(r * SQUARE_SIZE + SQUARE_SIZE/2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[r][c] == 2:
                # Draw player 2 piece (cross)
                start_pos1 = (c * SQUARE_SIZE + SQUARE_SIZE // 4, r * SQUARE_SIZE + SQUARE_SIZE // 4)
                end_pos1   = (c * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, r * SQUARE_SIZE + 3 * SQUARE_SIZE // 4)
                start_pos2 = (c * SQUARE_SIZE + SQUARE_SIZE // 4, r * SQUARE_SIZE + 3 * SQUARE_SIZE // 4)
                end_pos2   = (c * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, r * SQUARE_SIZE + SQUARE_SIZE // 4)
                pygame.draw.line(screen, color, start_pos1, end_pos1, CROSS_WIDTH)
                pygame.draw.line(screen, color, start_pos2, end_pos2, CROSS_WIDTH)

def get_next_open_row(board, col):
    """Return the index of the next available row in the given column (searching from bottom up)."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def mark_square(col, player):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = player

def is_valid_move(col):
    # A move is valid if the top row in that column is empty.
    return board[0][col] == 0

def is_board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == 0:
            return False
    return True

def check_win(player, check_board=board):
    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if (check_board[r][c] == player and 
                check_board[r][c+1] == player and 
                check_board[r][c+2] == player and 
                check_board[r][c+3] == player):
                return True
    # Check vertical win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (check_board[r][c] == player and 
                check_board[r+1][c] == player and 
                check_board[r+2][c] == player and 
                check_board[r+3][c] == player):
                return True
    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if (check_board[r][c] == player and 
                check_board[r+1][c+1] == player and 
                check_board[r+2][c+2] == player and 
                check_board[r+3][c+3] == player):
                return True
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if (check_board[r][c] == player and 
                check_board[r-1][c+1] == player and 
                check_board[r-2][c+2] == player and 
                check_board[r-3][c+3] == player):
                return True
    return False

def minimax(board, depth, is_maximizing):
    # Terminal conditions
    if check_win(2, board):
        return float('inf')
    elif check_win(1, board):
        return float('-inf')
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for col in range(COLUMNS):
            if is_valid_move(col):
                row = get_next_open_row(board, col)
                board[row][col] = 2
                score = minimax(board, depth + 1, False)
                board[row][col] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for col in range(COLUMNS):
            if is_valid_move(col):
                row = get_next_open_row(board, col)
                board[row][col] = 1
                score = minimax(board, depth + 1, True)
                board[row][col] = 0
                best_score = min(score, best_score)
        return best_score

def best_move():
    if is_board_full(board):
        return False

    best_score = -1000
    move = None
    for col in range(COLUMNS):
        if is_valid_move(col):
            row = get_next_open_row(board, col)
            board[row][col] = 2
            score = minimax(board, 0, False)
            board[row][col] = 0
            if score > best_score:
                best_score = score
                move = col
    if move is not None:
        mark_square(move, 2)
        return True
    return False

def restart_game():
    global board
    board = np.zeros((ROWS, COLUMNS))
    screen.fill(BLACK)
    draw_lines()

# Draw the initial grid
draw_lines()

# Game variables
player = 1    # human player
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            col = mouseX // SQUARE_SIZE

            if is_valid_move(col):
                # Human move (player 1)
                mark_square(col, 1)
                if check_win(1):
                    game_over = True
                else:
                    player = 2

                # AI move (player 2)
                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        else:
                            player = 1

                if is_board_full(board):
                    game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    # Redraw the board each frame
    screen.fill(BLACK)
    draw_lines()
    if not game_over:
        draw_figures()
    else:
        # If game is over, draw the winning board in a special color.
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)

    pygame.display.update()
