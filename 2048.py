import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SIZE = 4
WIDTH = 500
HEIGHT = 600
TILE_SIZE = WIDTH // SIZE
BORDER_WIDTH = 5
FONT = pygame.font.Font(None, 55)
LARGE_FONT = pygame.font.Font(None, 70)
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'background': (187, 173, 160),
    'board': (187, 173, 160),
    'text': (119, 110, 101),
    'score': (119, 110, 101)
}

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

def initialize_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

def draw_board(board, score):
    screen.fill(COLORS['background'])
    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            color = COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (c * TILE_SIZE + BORDER_WIDTH, r * TILE_SIZE + TILE_SIZE + BORDER_WIDTH, TILE_SIZE - 2 * BORDER_WIDTH, TILE_SIZE - 2 * BORDER_WIDTH))
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0) if value <= 4 else (255, 255, 255))
                text_rect = text.get_rect(center=(c * TILE_SIZE + TILE_SIZE / 2, r * TILE_SIZE + TILE_SIZE + TILE_SIZE / 2))
                screen.blit(text, text_rect)
    
    # Draw the score
    score_text = LARGE_FONT.render(f"Score: {score}", True, COLORS['score'])
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 20))

    pygame.display.update()

def move_left(board):
    new_board = []
    for row in board:
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        new_row.extend([0] * (SIZE - len(new_row)))
        new_board.append(new_row)
    return new_board

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved_board = move_left(reversed_board)
    return [row[::-1] for row in moved_board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed_board = transpose(board)
    moved_board = move_left(transposed_board)
    return transpose(moved_board)

def move_down(board):
    transposed_board = transpose(board)
    moved_board = move_right(transposed_board)
    return transpose(moved_board)

def can_merge(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if (c < SIZE - 1 and board[r][c] == board[r][c + 1]) or (r < SIZE - 1 and board[r][c] == board[r + 1][c]):
                return True
    return False

def game_over(board):
    return not any(0 in row for row in board) and not any(can_merge(board))

def boards_are_equal(board1, board2):
    for r in range(SIZE):
        for c in range(SIZE):
            if board1[r][c] != board2[r][c]:
                return False
    return True

def main():
    board = initialize_board()
    score = 0
    running = True
    while running:
        draw_board(board, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                old_board = [row[:] for row in board]
                if event.key == pygame.K_w:
                    board = move_up(board)
                elif event.key == pygame.K_a:
                    board = move_left(board)
                elif event.key == pygame.K_s:
                    board = move_down(board)
                elif event.key == pygame.K_d:
                    board = move_right(board)
                
                if not boards_are_equal(old_board, board):
                    add_new_tile(board)
                    score += sum(sum(row) for row in board)  # Update the score

                if game_over(board):
                    draw_board(board, score)
                    game_over_text = LARGE_FONT.render("Game Over!", True, (255, 0, 0))
                    screen.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    running = False
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
