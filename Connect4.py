class Connect4:
    def __init__(self, rows=6, cols=7, win_condition=4):
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition

        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1
        self.winner = None
        self.total_moves = {1: 0, 2: 0}
        self.max_moves = 500

    def print_board(self):
        for row in self.board:
            print("|".join(str(cell) for cell in row))
        print()

    def check_full_board(self):
        if self.total_moves[1] + self.total_moves[2] == self.rows * self.cols:
            self.winner = 0

    def add_disc(self, col):
        if self.winner is not None:
            return self.winner

        self.total_moves[self.current_player] += 1
        if self.total_moves[self.current_player] > self.max_moves:
            if self.total_moves[3 - self.current_player] == self.max_moves:
                self.winner = 0
            else:
                self.winner = 3 - self.current_player
            return self.winner

        if col < 0 or col >= self.cols:
            self.winner = 3 - self.current_player
            return self.winner

        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player

                if self.check_winner(row, col):
                    self.winner = self.current_player
                    return self.winner
                else:
                    self.current_player = 3 - self.current_player
                self.check_full_board()
                return None
        self.winner = 3 - self.current_player
        return self.winner

    def check_winner(self, row, col):
        # Check all directions for a win condition
        return (
            self.check_direction(row, col, 1, 0)
            or self.check_direction(row, col, 0, 1)
            or self.check_direction(row, col, 1, 1)
            or self.check_direction(row, col, 1, -1)
        )

    def check_direction(self, row, col, delta_row, delta_col):
        disc = self.board[row][col]
        count = 1

        # Check both directions for a win condition
        count += self.count_consecutive(row, col, delta_row, delta_col, disc)
        count += self.count_consecutive(row, col, -delta_row, -delta_col, disc)

        return count >= self.win_condition

    def count_consecutive(self, row, col, delta_row, delta_col, disc):
        count = 0
        for i in range(1, self.win_condition):
            r = row + i * delta_row
            c = col + i * delta_col
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == disc:
                count += 1
            else:
                break
        return count
