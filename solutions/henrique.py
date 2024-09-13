from random import randint
import sys
import select
import time


# Define the board and check victory condition
def create_board(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Display the entire board
    print("\nCurrent Board:")
    for row in board:
        print(" ".join([str(x) if x != 0 else "." for x in row]))
    print("\n")


def is_valid_move(board, col):
    return 0 <= col < len(board[0]) and board[0][col] == 0


def get_next_open_row(board, col):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def winning_move(board, piece, needed):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - needed + 1):
            if all(board[r][c + i] == piece for i in range(needed)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - needed + 1):
            if all(board[r + i][c] == piece for i in range(needed)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - needed + 1):
        for c in range(cols - needed + 1):
            if all(board[r + i][c + i] == piece for i in range(needed)):
                return True

    # Check negatively sloped diagonals
    for r in range(needed - 1, rows):
        for c in range(cols - needed + 1):
            if all(board[r - i][c + i] == piece for i in range(needed)):
                return True

    return False


# Game parameters
def get_game_params(game_type):
    if game_type == 1:
        return 7, 6, 4  # Columns, Rows, Needed to win
    elif game_type == 2:
        return 7, 100, 4
    elif game_type == 3:
        return 70, 10, 4
    elif game_type == 4:
        return 140, 120, 5


def play_game():

    color, game_type = map(int, input().split())

    # Get game-specific parameters
    cols, rows, needed = get_game_params(game_type)

    # Create board
    board = create_board(rows, cols)

    # Player pieces: color 1 uses 1, color 2 uses 2
    player_piece = color
    opponent_piece = 2 if color == 1 else 1

    # Game loop
    first_move = True if color == 2 else False
    while True:
        opponent_col = randint(0, cols - 1)
        print(opponent_col + 1)
        continue
        # Player's move
        if first_move:
            chosen_col = int(input()) - 1  # Convert to 0-indexed
            if is_valid_move(board, chosen_col):
                row = get_next_open_row(board, chosen_col)
                drop_piece(board, row, chosen_col, player_piece)
                if winning_move(board, player_piece, needed):
                    print("\nYou win! Congratulations!")
                    break

        # Opponent's move (randomly generated)
        opponent_col = randint(0, cols - 1)
        first_move = True
        if is_valid_move(board, opponent_col):
            row = get_next_open_row(board, opponent_col)
            drop_piece(board, row, opponent_col, opponent_piece)
            print(row + 1)
            if winning_move(board, opponent_piece, needed):
                print("\nOpponent wins! Game over.")
                break
    while True:
        print(1)


def start_game():
    while True:
        play_game()


if __name__ == "__main__":
    start_game()
