import subprocess
from subprocess import PIPE
import time
import re

from Connect4 import Connect4


def extract_output(s):
    numbers = re.findall(r"\d+", s)
    if len(numbers) == 0:
        return None
    return numbers[0]


def print_log(log, file):
    print(log)
    print(log, file=file)


def print_board(board, file):
    for row in board:
        print("|".join(str(cell) for cell in row))
        print("|".join(str(cell) for cell in row), file=file)
    print(file=file)
    print()


def play_game(playerA, playerB, path_log, game_type):
    nameA, programA = playerA
    nameB, programB = playerB

    procA = subprocess.Popen(programA, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    procB = subprocess.Popen(programB, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    inA = f"{1} {game_type}\n"
    inB = f"{2} {game_type}\n"

    procA.stdin.write(bytes(inA, "utf-8"))
    procA.stdin.flush()
    procB.stdin.write(bytes(inB, "utf-8"))
    procB.stdin.flush()

    needed = 4
    if game_type == 1:
        k, r = 7, 6
    elif game_type == 2:
        k, r = 7, 100
    elif game_type == 3:
        k, r = 70, 10
    elif game_type == 4:
        k, r = 140, 120
        needed = 5

    game = Connect4(r, k, needed)

    with open(path_log, "w") as f:
        while game.winner is None:
            outA = procA.stdout.readline().decode()

            int_out = extract_output(outA)
            if int_out is None:
                game.winner = 2
                break
            print_log(f"{nameA} plays: {int_out}", f)
            playA = int(outA) - 1
            game.add_disc(playA)

            if game.winner is not None:
                break

            procB.stdin.write(bytes(outA, "utf-8"))
            procB.stdin.flush()
            outB = procB.stdout.readline().decode()
            int_out = extract_output(outB)
            if int_out is None:
                game.winner = 1
                break
            print_log(f"{nameB} plays: {int_out}", f)

            playB = int(outB) - 1
            game.add_disc(playB)
            procA.stdin.write(bytes(outB, "utf-8"))
            procA.stdin.flush()

        print_log("\nFinal Board:\n", f)
        print_board(game.board, f)
        if game.winner == 0:
            print_log("Draw\n", f)
            procA.kill()
            procB.kill()
            return 0
        else:
            winner = nameA if game.winner == 1 else nameB
            print_log(f"Winner: {winner}", f)
            procA.kill()
            procB.kill()
            return winner
