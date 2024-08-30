# Programming Challenge 2024

This time the challenge consists of creating a program that can play a game of Connect 4.<br>
Each program will play 3 different games of Connect 4 against another participant's program.<br>

## Connect 4 game format 

Connect 4 is a two-player connection game in which the players first choose a color and then take turns dropping colored discs from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. 

## The challenge ##

For this challenge, 3 different types of connect 4 games will be played.  
1. The first game will be played with the standard rules. 
2. The second game will be played in a 1400 column by 1200 row grid.
3. The third game will be in the 1400 column by 1200 row grid, but with the winning condition being 5 in a row/column/diagonal instead of 4.

Each program will play 10 rounds of each type of game against another participant's program. 3 points will be awarded for each win, 1 point for each draw and 0 points for each loss. 

The participant's programs will compete in a format all vs all, and the program with the most points at the end of the competition will be the winner.

As a couple of additional rules:
- The program must be able to play the game without human intervention.
- The use of backtracking algorithms or memoization of states is **NOT ALLOWED.** Since this approach would make the game trivial to solve.
- The time limit for each move is 0.1 seconds.

## Behavior of the program 
The program should read two initial integer values $C$ and $G$, representing the color of the player and the type of game, respectively. The color of the player will be 1 or 2, and the type of game will be 1, 2 or 3.

Player with color 1 will always start the game.
It is guaranteed that each program will be given 5 times the color 1 and 5 times the color 2 for each type of game.

Player with color 1 shall have the first turn, thus is the first program to give an output.

For each turn the program should first read a value $1 \leq x \leq K$, where $K$ is the number of columns in the grid. This value represents the column where the previous player placed the disc.
After that, the program shall output an integer value $1 \leq y \leq K$, where $K$ is the number of columns in the grid. This value represents the column where the player wants to place his disc.

Only for the first turn of the game, the program will not read the value of $x$.

In the case the program wishes to insert a disc in a column that is already full, the victory will automatically be given to the other player. Thus each program should at all points save the state of the game.

## Languages accepted ##
- Python
- C++
- Java
- C#

Only standard libraries are allowed. The use of external libraries is not allowed.
