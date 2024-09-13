#include <cstdlib>
#include <ctime>
#include <iostream>
#include <random>
#include <vector>


using namespace std;

class Connect4 {
public:
    int rows, cols, winCondition;
    vector<vector<int>> board;

    Connect4(int r, int c, int w) : rows(r), cols(c), winCondition(w) {
        board = vector<vector<int>>(rows, vector<int>(cols, 0));
    }

    void printBoard() {
        cout << endl << "Current Board State:" << endl;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (board[r][c] == 0)
                    cout << ". ";
                else if (board[r][c] == 1)
                    cout << "X ";
                else
                    cout << "O ";
            }
            cout << endl;
        }
        for (int c = 1; c <= cols; c++) {
            cout << c << " ";
        }
        cout << endl;
    }

    bool isColumnFull(int col) {
        return board[0][col] != 0;
    }

    bool placeDisc(int col, int player) {
        if (isColumnFull(col))
            return false;
        for (int r = rows - 1; r >= 0; r--) {
            if (board[r][col] == 0) {
                board[r][col] = player;
                return true;
            }
        }
        return false;
    }

    bool checkWin(int lastCol, int player) {
        int lastRow = -1;
        for (int r = 0; r < rows; r++) {
            if (board[r][lastCol] == player) {
                lastRow = r;
                break;
            }
        }

        if (lastRow == -1)
            return false;

        return checkDirection(lastRow, lastCol, 0, 1, player) ||
               checkDirection(lastRow, lastCol, 1, 0, player) ||
               checkDirection(lastRow, lastCol, 1, 1, player) ||
               checkDirection(lastRow, lastCol, 1, -1, player);
    }

    bool checkDirection(int row, int col, int dRow, int dCol, int player) {
        int count = 0;
        for (int i = 0; i < winCondition; i++) {
            int r = row + i * dRow;
            int c = col + i * dCol;
            if (r >= 0 && r < rows && c >= 0 && c < cols && board[r][c] == player) {
                count++;
            } else {
                break;
            }
        }
        for (int i = 1; i < winCondition; i++) {
            int r = row - i * dRow;
            int c = col - i * dCol;
            if (r >= 0 && r < rows && c >= 0 && c < cols && board[r][c] == player) {
                count++;
            } else {
                break;
            }
        }
        return count >= winCondition;
    }

    int getBestMove(int player) {
        vector<int> columnPriority;
        vector<int> claimEvenPriority;

        int centerColumn = cols / 2;

        // odd-even ranking
        if (player == 1) {
            for (int i = 0; i < cols; i++) {
                if (i % 2 == 0)
                    columnPriority.push_back(i);
            }
            for (int i = 0; i < cols; i++) {
                if (i % 2 != 0)
                    columnPriority.push_back(i);
            }
        } else {
            for (int i = 0; i < cols; i++) {
                if (i % 2 != 0)
                    columnPriority.push_back(i);
            }
            for (int i = 0; i < cols; i++) {
                if (i % 2 == 0)
                    columnPriority.push_back(i);
            }
        }

        // 1. play center
        if (!isColumnFull(centerColumn)) {
            return centerColumn + 1;
        }

        // 2. play to win
        for (int c = 0; c < cols; c++) {
            if (!isColumnFull(c)) {
                placeDisc(c, player);
                if (checkWin(c, player)) {
                    removeDisc(c);
                    return c + 1;
                }
                removeDisc(c);
            }
        }

        // 3. play to not lose
        int opponent = (player == 1) ? 2 : 1;
        for (int c = 0; c < cols; c++) {
            if (!isColumnFull(c)) {
                placeDisc(c, opponent);
                if (checkWin(c, opponent)) {
                    removeDisc(c);
                    return c + 1;
                }
                removeDisc(c);
            }
        }

        // 4. play to claim-even or claim-odd
        if (player == 1) {
            for (int c = 0; c < cols; c++) {
                if (c % 2 != 0 && !isColumnFull(c)) {
                    for (int r = rows - 2; r >= 0; r -= 2) {
                        if (board[r][c] == 0 && board[r + 1][c] != 0) {
                            return c + 1;
                        }
                    }
                }
            }
        } else {
            for (int c = 0; c < cols; c++) {
                if (c % 2 == 0 && !isColumnFull(c)) {
                    for (int r = rows - 2; r >= 0; r -= 2) {
                        if (board[r][c] == 0 && board[r + 1][c] != 0) {
                            return c + 1;
                        }
                    }
                }
            }
        }

        // 5. odd even
        for (int c : columnPriority) {
            if (!isColumnFull(c)) {
                return c + 1;
            }
        }

        // 6. random is great
        vector<int> availableColumns;
        for (int c = 0; c < cols; c++) {
            if (!isColumnFull(c)) {
                availableColumns.push_back(c);
            }
        }
        if (!availableColumns.empty()) {
            random_device rd;
            mt19937 gen(rd());
            uniform_int_distribution<> distr(0, availableColumns.size() - 1);
            int randomIndex = distr(gen);
            return availableColumns[randomIndex] + 1;
        }

        return 1;
    }

    void removeDisc(int col) {
        for (int r = 0; r < rows; r++) {
            if (board[r][col] != 0) {
                board[r][col] = 0;
                break;
            }
        }
    }
};

int main() {
    int player, gameType;
    cin >> player >> gameType;

    int rows, cols, winCondition;
    if (gameType == 1) {
        rows = 6;
        cols = 7;
        winCondition = 4;
    } else if (gameType == 2) {
        rows = 100;
        cols = 7;
        winCondition = 4;
    } else if (gameType == 3) {
        rows = 10;
        cols = 70;
        winCondition = 4;
    } else if (gameType == 4) {
        rows = 120;
        cols = 140;
        winCondition = 5;
    }

    Connect4 game(rows, cols, winCondition);

    int prevMove = -1;
    for (int turn = 0; turn < 500; turn++) {
        if (prevMove != -1) {
            int lastMoveColumn;
            cin >> lastMoveColumn;
            lastMoveColumn--;
            if (!game.placeDisc(lastMoveColumn, 3 - player)) {
                cout << "Error: Invalid move by opponent." << endl;
                return 1;
            }
        }

        int move = game.getBestMove(player);
        cout << move << endl;

        game.placeDisc(move - 1, player);
        prevMove = move;
    }
    return 0;
}