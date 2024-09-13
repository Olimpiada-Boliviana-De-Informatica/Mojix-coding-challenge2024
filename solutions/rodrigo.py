class Connect4:
    def __init__(self, rows, cols, win_condition):
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.column_heights = [0] * cols

    def is_valid_move(self, col):
        return self.column_heights[col] < self.rows

    def make_move(self, player, col):
        if not self.is_valid_move(col):
            raise ValueError("Invalid move")
        row = self.column_heights[col]
        self.grid[row][col] = player
        self.column_heights[col] += 1
        return row, col

    def undo_move(self, col):
        if self.column_heights[col] == 0:
            raise ValueError("No move to undo")
        row = self.column_heights[col] - 1
        self.grid[row][col] = 0
        self.column_heights[col] -= 1

    def get_best_move(self, player):
        best_score = -float('inf')
        best_col = None
        for col in range(self.cols):
            if self.is_valid_move(col):
                row, _ = self.make_move(player, col)
                score = self.evaluate_board(player)
                if self.check_winner(player, row, col):
                    self.undo_move(col)
                    return col + 1  # Return winning move directly
                self.undo_move(col)
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col + 1 if best_col is not None else None

    def check_winner(self, player, row, col):

        return (self.check_line(player, row, col, 1, 0) or  # Horizontal
                self.check_line(player, row, col, 0, 1) or  # Vertical
                self.check_line(player, row, col, 1, 1) or  # Diagonal /
                self.check_line(player, row, col, 1, -1))   # Diagonal \

    def check_line(self, player, row, col, d_row, d_col):
        count = 1
        for direction in [1, -1]:
            r, c = row, col
            while 0 <= r + direction * d_row < self.rows and 0 <= c + direction * d_col < self.cols:
                r += direction * d_row
                c += direction * d_col
                if self.grid[r][c] == player:
                    count += 1
                else:
                    break
        return count >= self.win_condition

    def score_horizontal(self, player):
        score = 0
        for row in range(self.rows):
            row_array = self.grid[row]
            for col in range(self.cols - (self.win_condition - 1)):
                window = row_array[col:col + self.win_condition]
                score += self.evaluate_window(window, player)
        return score

    def score_vertical(self, player):
        score = 0
        for col in range(self.cols):
            col_array = [self.grid[row][col] for row in range(self.rows)]
            for row in range(self.rows - (self.win_condition - 1)):
                window = col_array[row:row + self.win_condition]
                score += self.evaluate_window(window, player)
        return score

    def score_diagonal(self, player):
        score = 0
        # Positive slope diagonal (/)
        for row in range(self.rows - (self.win_condition - 1)):
            for col in range(self.cols - (self.win_condition - 1)):
                window = [self.grid[row + i][col + i] for i in range(self.win_condition)]
                score += self.evaluate_window(window, player)

        # Negative slope diagonal (\)
        for row in range(self.rows - (self.win_condition - 1)):
            for col in range(self.win_condition - 1, self.cols):
                window = [self.grid[row + i][col - i] for i in range(self.win_condition)]
                score += self.evaluate_window(window, player)

        return score

    def evaluate_board(self, player):
        score = 0

        center_col_index = self.cols // 2
        center_array = [self.grid[row][center_col_index] for row in range(self.rows)]
        center_count = center_array.count(player)
        score += center_count * 3

        score += self.score_horizontal(player)
        score += self.score_vertical(player)
        score += self.score_diagonal(player)

        return score

    def evaluate_window(self, window, player):
        score = 0
        opponent = 2 if player == 1 else 1

        if window.count(player) == self.win_condition:  # Win condition
            score += 200
        elif window.count(player) == self.win_condition - 1 and window.count(0) == 1:  # 3 in a row, one empty
            score += 10
        elif window.count(player) == self.win_condition - 2 and window.count(0) == 2:  # 2 in a row, two empty
            score += 5

        if window.count(opponent) == self.win_condition - 1 and window.count(0) == 1:
            score -= 80

        if window.count(opponent) == 2 and window.count(0) == 2:

            empty_positions = [i for i, x in enumerate(window) if x == 0]
            if len(empty_positions) == 2:
                if (empty_positions[1] - empty_positions[0]) == 3:
                    score -= 50
        return score

    def print_grid(self):
        for row in self.grid:
            print(row)
        print()

def play_game():
    C, G = map(int, input().split())

    if G == 2:
        rows, cols, win_condition = 100, 7, 4
    elif G == 3:
        rows, cols, win_condition = 10, 70, 4
    elif G == 4:
        rows, cols, win_condition = 120, 140, 5
    else:
        rows, cols, win_condition = 6, 7, 4

    game = Connect4(rows, cols, win_condition)

    if C == 2:
        previous_move = int(input()) - 1
        game.make_move(3 - C, previous_move)

    while True:

        best_move = game.get_best_move(C)
        if best_move is None:
            print("It's a tie!")
            return

        print(best_move)

        row, _ = game.make_move(C, best_move - 1)

        if game.check_winner(C, row, best_move - 1):
            print(f"Player {C} wins!")
            return

        previous_move = int(input()) - 1

        row, _ = game.make_move(3 - C, previous_move)

        if game.check_winner(3 - C, row, previous_move):
            print(f"Player {3 - C} wins!")
            return



play_game()