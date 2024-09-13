import java.util.Scanner;

public class Connect4Game {
    private int rows;
    private int cols;
    private int winCondition;
    private int[][] board;
    private int currentPlayer;
    private int moveCount;

    public Connect4Game(int gameType, int playerColor) {
        // Initialize game based on the type
        switch(gameType) {
            case 1:
                this.rows = 6;
                this.cols = 7;
                this.winCondition = 4;  // 4 in a row for the first 3 games
                break;
            case 2:
                this.rows = 100;
                this.cols = 7;
                this.winCondition = 4;
                break;
            case 3:
                this.rows = 10;
                this.cols = 70;
                this.winCondition = 4;
                break;
            case 4:
                this.rows = 120;
                this.cols = 140;
                this.winCondition = 5;  // 5 in a row for the fourth game
                break;
        }
        this.board = new int[rows][cols];
        this.currentPlayer = playerColor;
        this.moveCount = 0;
    }

    // Method to drop a disc in the selected column
    public boolean dropDisc(int col, int player) {
        for (int row = rows - 1; row >= 0; row--) {
            if (board[row][col] == 0) {
                board[row][col] = player;
                moveCount++;
                return true;
            }
        }
        return false; // Column is full
    }

    // Check if the last move is a winning move
    public boolean checkWin(int row, int col, int player) {
        return (checkDirection(row, col, 1, 0, player) + checkDirection(row, col, -1, 0, player) >= winCondition - 1) ||  // Horizontal
               (checkDirection(row, col, 0, 1, player) + checkDirection(row, col, 0, -1, player) >= winCondition - 1) ||  // Vertical
               (checkDirection(row, col, 1, 1, player) + checkDirection(row, col, -1, -1, player) >= winCondition - 1) || // Diagonal /
               (checkDirection(row, col, 1, -1, player) + checkDirection(row, col, -1, 1, player) >= winCondition - 1);   // Diagonal \
    }

    // Count consecutive discs in one direction
    private int checkDirection(int row, int col, int rowDir, int colDir, int player) {
        int count = 0;
        for (int i = 1; i < winCondition; i++) {
            int newRow = row + i * rowDir;
            int newCol = col + i * colDir;
            if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols && board[newRow][newCol] == player) {
                count++;
            } else {
                break;
            }
        }
        return count;
    }

    // Display the board (useful for debugging)
    public void printBoard() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    // Check if placing a disc in a column can result in a win for the given player
    public boolean canWin(int col, int player) {
        for (int row = rows - 1; row >= 0; row--) {
            if (board[row][col] == 0) {
                board[row][col] = player; // Temporarily place the disc
                boolean isWinningMove = checkWin(row, col, player);
                board[row][col] = 0; // Remove the disc
                return isWinningMove;
            }
        }
        return false; // Column is full, cannot win here
    }

    // Strategy to determine the next move
    public int getNextMove() {
        // 1. Try to win by placing our piece in any available column
        for (int col = 0; col < cols; col++) {
            if (!isColumnFull(col) && canWin(col, currentPlayer)) {
                return col + 1; // If we can win, place here
            }
        }

        // 2. Block the opponent if they are about to win
        int opponent = 3 - currentPlayer; // Opponent is the other player
        for (int col = 0; col < cols; col++) {
            if (!isColumnFull(col) && canWin(col, opponent)) {
                return col + 1; // If the opponent is about to win, block them
            }
        }

        // 3. If neither we nor the opponent can win immediately, pick the first available column
        for (int col = 0; col < cols; col++) {
            if (!isColumnFull(col)) {
                return col + 1; // Pick the first available column
            }
        }
        return 1; // Fallback to the first column
    }

    public boolean isColumnFull(int col) {
        return board[0][col] != 0;
    }

    public boolean isBoardFull() {
        for (int col = 0; col < cols; col++) {
            if (!isColumnFull(col)) {
                return false;
            }
        }
        return true;
    }

    public boolean isTie() {
        return moveCount >= 500 || isBoardFull();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Read initial input: color and game type
        int color = sc.nextInt(); // 1 or 2 (our player color)
        int gameType = sc.nextInt(); // 1, 2, 3 or 4 (game type)

        Connect4Game game = new Connect4Game(gameType, color);
        
        int lastMove = -1;
        boolean gameOver = false;
        while (!gameOver) {
            if (lastMove != -1) {
                // Read the opponent's last move (except for the first turn)
                lastMove = sc.nextInt();
                
                // Check if opponent made an invalid move (dropped in full column)
                if (game.isColumnFull(lastMove - 1)) {
                    System.out.println("Invalid move by opponent. You win!");
                    gameOver = true;
                    continue;
                }

                // Place opponent's piece
                game.dropDisc(lastMove - 1, 3 - color);  // Place opponent's piece
            }
            
            // Make our move
            if (game.isTie()) {
                System.out.println("Tie!");
                break;
            }
            
            int ourMove = game.getNextMove();
            game.dropDisc(ourMove - 1, color);
            
            // Output our move
            System.out.println(ourMove);
            lastMove = ourMove;

            // Check if we won with this move
            if (game.checkWin(ourMove - 1, ourMove - 1, color)) {
                System.out.println("We win!");
                gameOver = true;
            }
        }
    }
}
