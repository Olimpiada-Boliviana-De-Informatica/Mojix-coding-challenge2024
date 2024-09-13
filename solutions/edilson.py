from random import randint

# Configuración inicial
c, g = map(int, input().split())
needed = 4 if g != 4 else 5  # 4 en línea, excepto en el juego 4
if g == 1:
    k, r = 7, 6
elif g == 2:
    k, r = 7, 100
elif g == 3:
    k, r = 70, 10
elif g == 4:
    k, r = 140, 120

board = [[0 for _ in range(k)] for _ in range(r)]  # Inicializa el tablero vacío

# Funciones auxiliares
def is_valid_move(col):
    return board[0][col] == 0  # Verifica si la columna no está llena

def drop_disc(col, player):
    for row in range(r - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            break

def block_opponent_vertical(col, needed):
    """Evalúa si el oponente está cerca de ganar verticalmente y coloca una ficha para bloquear"""
    opponent = 2
    count = 0
    for row in range(r - 1, -1, -1):
        if board[row][col] == opponent:
            count += 1
        else:
            break
    if count == needed - 1:  # Si el oponente está a un movimiento de ganar verticalmente
        drop_disc(col, 1)
        print(col + 1)  # Responde con la columna bloqueada
        return True
    return False

# Turno inicial si eres jugador 1
if c == 1:
    chosen_col = randint(0, k - 1)
    drop_disc(chosen_col, 1)
    print(chosen_col + 1)

# Bucle principal del juego
while True:
    adversary_col = int(input()) - 1
    drop_disc(adversary_col, 2)

    # Intenta bloquear al oponente verticalmente
    if block_opponent_vertical(adversary_col, needed):
        continue  # Si ya bloqueó, pasa al siguiente turno

    # Si no es necesario bloquear, coloca una ficha aleatoriamente
    chosen_col = randint(0, k - 1)
    while not is_valid_move(chosen_col):
        chosen_col = randint(0, k - 1)
    drop_disc(chosen_col, 1)
    print(chosen_col + 1)
