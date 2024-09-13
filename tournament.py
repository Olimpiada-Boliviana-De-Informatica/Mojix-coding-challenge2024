from versus import play_game
from itertools import combinations

players = (
    ("henrique", "python solutions/henrique.py"),
    ("rodrigo", "python solutions/rodrigo.py"),
    ("oscar", "python solutions/oscar.py"),
    ("edilson", "python solutions/edilson.py"),
    ("rodolfo", "./solutions/rodolfo.exe"),
    ("hagi", "./solutions/hagi.exe"),
    ("victor", "java Connect4Game"),
    ("andre", "java Connect4"),
)

points = {name: 0 for name, _ in players}


def add_points(nameA, nameB, winner, game_type):
    first, second = nameA, nameB
    if nameA > nameB:
        first, second = nameB, nameA

    with open(f"logs/{game_type}/RESULTS_{first}vs{second}.txt", "a") as f:
        print(f"{nameA} vs {nameB} -> {"Draw" if winner == 0 else winner}", file=f)

    if winner == 0:
        points[nameA] += 1
        points[nameB] += 1

        return

    points[winner] += 3


for game_type in range(4, 5):
    directory = f"logs/{game_type}"
    points = {name: 0 for name, _ in players}
    for playerA, playerB in combinations(players, 2):
        # 5 Games for each player being the first to play
        for i in range(5):
            path_log = f"{directory}/{playerA[0]}_vs_{playerB[0]}_{i}.txt"
            print(f"Playing {playerA[0]} vs {playerB[0]}")
            winner = play_game(playerA, playerB, path_log, game_type)
            add_points(playerA[0], playerB[0], winner, game_type)

        for i in range(5, 10):
            path_log = f"{directory}/{playerB[0]}_vs_{playerA[0]}_{i}.txt"
            print(f"Playing {playerB[0]} vs {playerA[0]}")
            winner = play_game(playerB, playerA, path_log, game_type)
            add_points(playerB[0], playerA[0], winner, game_type)
    with open(f"logs/RESULTS_{game_type}.txt", "w") as f:
        print(points, file=f)
