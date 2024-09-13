from random import randint

def init_matrix(k, r):
    matrix = [[0 for _ in range(k)] for _ in range(r)]
    return matrix

def init_v_available(k, r):
    v_available = []
    for indx in range(k):
        v_available.append([r-1, indx])
    return v_available

def check_grid(matrix, x, y):
    if matrix[x][y] == 1:
        return 2
    elif matrix[x][y] == 2:
        return 0
    elif matrix[x][y] == 0:
        return 1

def find_window_vertical(x, y, k, r):
    left = True
    right = True
    a = 0
    b = 0
    for i in range(4):
        if x + i < r and right == True and check_grid(matrix, x + i, y) != 0:
            b = x + i
        else:
            right = False
        if x - i >= 0 and left == True and check_grid(matrix, x - i, y) != 0:
            a = x - i
        else:
            left = False
    return a,b

def find_window_horizontal(x, y, k, r):
    left = True
    right = True
    a = 0
    b = 0
    for i in range(4):
        if y + i < k and right == True and check_grid(matrix, x, y + i) != 0:
            b = y + i
        else:
            right = False
        if y - i >= 0 and left == True and check_grid(matrix, x, y - i) != 0:
            a = y - i
        else:
            left = False
    return a,b

def find_window_diagonal_1(x, y, k, r):
    left = True
    right = True
    a = 0
    b = 0
    c = 0
    d = 0
    for i in range(4):
        
        if y + i < k and x + i < r and right == True and check_grid(matrix, x + i, y + i) != 0:
            c = y + i
            d = x + i
        else:
            right = False
        if y - i >= 0 and x - i >= 0 and left == True and check_grid(matrix, x - i, y - i) != 0:
            a = y - i
            b = x - i
        else:
            left = False
    return a,b,c,d

def find_window_diagonal_2(x, y, k, r):
    left = True
    right = True
    a = 0
    b = 0
    c = 0
    d = 0
    for i in range(4):
        
        if y + i < k and x - i >= 0 and right == True and check_grid(matrix, x - i, y + i) != 0:
            c = y + i
            d = x - i
        else:
            right = False
        if y - i >= 0 and x + i <= r and left == True and check_grid(matrix, x + i, y - i) != 0:
            a = y - i
            b = x + i
        else:
            left = False
    return a,b,c,d


def check_pos_points_horizontal(matrix, x, y, k ,r):
    a, b = find_window_horizontal(x, y, k, r)
    subs = abs(a - b) + 1
    total = 0
    if subs <= 4:
        for i in range(a, b + 1):
            total = total + check_grid(matrix, x, i)
    else:
        if a + 4 <= b:
            for i in range(a, a+5):    
                total = total + check_grid(matrix, x, i)
                    
        if a + 5 <= b:
            for i in range(a + 1, a + 6):
                total = total + check_grid(matrix, x, i)

        if a + 6 <= b:
            for i in range(a + 2, a + 7):
                total = total + check_grid(matrix, x, i)

        if a + 7 <= b:
            for i in range(a + 3, a + 8):
                total = total + check_grid(matrix, y, i)

    return total

def check_pos_points_vertical(matrix, x, y, k ,r):
    a, b = find_window_vertical(x, y, k, r)
    subs = abs(a - b) + 1
    total = 0
    if subs <= 4:
        for i in range(a, b + 1):
            total = total + check_grid(matrix, i, y)
    else:
        if a + 4 <= b:
            for i in range(a, a+5):    
                total = total + check_grid(matrix, i, y)
                    
        if a + 5 <= b:
            for i in range(a + 1, a + 6):
                total = total + check_grid(matrix, i, y)

        if a + 6 <= b:
            for i in range(a + 2, a + 7):
                total = total + check_grid(matrix, i, y)

        if a + 7 <= b:
            for i in range(a + 3, a + 8):
                total = total + check_grid(matrix, i, y)
    return total

def check_pos_points_diagonal_1(matrix, x, y, k ,r):
    a, b, c, d = find_window_diagonal_1(x, y, k, r)
    subs = max(a-c, b-d) + 1
    total = 0
    aux = 0
    if subs <= 4:
        for i in range(a, c):
            total = total + check_grid(matrix, a + aux, b + aux)
            aux+=1
    else:
        aux = 0
        if a + 4 <= c:
            for i in range(a, c+5):    
                total = total + check_grid(matrix, a + aux, b + aux)
                aux+=1

        aux = 0            
        if a + 5 <= c:
            for i in range(a + 1, c + 6):
                total = total + check_grid(matrix, a + 1 + aux, b + 1 + aux)
                aux+=1
        
        aux = 0
        if a + 6 <= c:
            for i in range(a + 2, c + 7):
                total = total + check_grid(matrix, a + 2 + aux, b + 2 + aux)
                aux+=1

        aux = 0
        if a + 7 <= c:
            for i in range(a + 3, c + 8):
                total = total + check_grid(matrix, a + 3 + aux, b + 3 + aux)
                aux+=1
    return total

def check_pos_points_diagonal_2(matrix, x, y, k ,r):
    a, b, c, d = find_window_diagonal_1(x, y, k, r)
    subs = max(a-c, b-d) + 1
    total = 0
    aux = 0
    if subs <= 4:
        for i in range(a, c):
            total = total + check_grid(matrix, a + aux, b - aux)
            aux+=1
    else:
        aux = 0
        if a + 4 <= c:
            for i in range(a, c+5):    
                total = total + check_grid(matrix, a + aux, b - aux)
                aux+=1

        aux = 0            
        if a + 5 <= c:
            for i in range(a + 1, c + 6):
                total = total + check_grid(matrix, a + 1 + aux, b - 1 - aux)
                aux+=1
        
        aux = 0
        if a + 6 <= c:
            for i in range(a + 2, c + 7):
                total = total + check_grid(matrix, a + 2 + aux, b - 2 - aux)
                aux+=1

        aux = 0
        if a + 7 <= c:
            for i in range(a + 3, c + 8):
                total = total + check_grid(matrix, a + 3 + aux, b - 3 - aux)
                aux+=1
    return total

def update_v_available_matrix(matrix, v_available, x, y):
    for index in range(len(v_available)):
        if v_available[index][0] == x and v_available[index][1] == y:
            if x >= 0:
                matrix[x][y] = 1
            if x - 1 < 0:
                v_available[index][0] = -1
            else:
                v_available[index][0] = x - 1
    #print("av", v_available)

def update_v_available_matrix_oponent(matrix, v_available, column):
    for index in range(len(v_available)):
        if v_available[index][1] == column:
            x = v_available[index][0]
            y = v_available[index][1]
            if x >= 0:
                matrix[x][y] = 2
            if x - 1 < 0:
                v_available[index][0] = -1
            else:
                v_available[index][0] = x - 1
    #print("avop", v_available)

# we have to fill the matrix with the opponent move if we are not the first player
# here we assume that the matrix is filled and v_available is updated
def print_ma(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end="")
        print()

def copy_ma(matrix, k, r):
    matrix2 = [[0 for _ in range(k)] for _ in range(r)]
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix2[i][j] = matrix[i][j]
    return matrix2

def find_opt_col(v_available, matrix, k, r):
    max_points = -1
    best_x = -1
    best_y = -1
    for pos in v_available:
        x = pos[0]
        y = pos[1]
        if x == -1:
            continue
        total = 0
        total+=check_pos_points_horizontal(matrix, x, y, k, r)
        total+=check_pos_points_vertical(matrix, x, y, k, r)
        total+=check_pos_points_diagonal_1(matrix, x, y, k, r)
        total+=check_pos_points_diagonal_2(matrix, x, y, k, r)

        matrix2 = copy_ma(matrix, k, r)
        arr2 = copy_ma(v_available, 2, k)
        for i in range(len(matrix2)):
            for j in range(len(matrix2[i])):
                if matrix2[i][j] == 1:
                    matrix2[i][j] == 2
                if matrix2[i][j] == 2:
                    matrix2[i][j] == 1

        if total > max_points:
            max_points = total
            best_x = x
            best_y = y
    if best_x == -1:
        return -1, -1
    update_v_available_matrix(matrix, v_available, best_x, best_y)
    return best_x, best_y

def check_next_mv(v_available, matrix, k, r):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                matrix[i][j] == 2
            if matrix[i][j] == 2:
                matrix[i][j] == 1
    return find_opt_col(v_available, matrix, k, r)

c, g = map(int, input().split())

needed = 4
winner = False
k = 0
r = 0
if g == 1:
    k, r = 7, 6
elif g == 2:
    k, r = 7, 100
elif g == 3:
    k, r = 70, 10
elif g == 4:
    k, r = 140, 120
    needed = 5

matrix = init_matrix(k, r)
#check for available positions to play
v_available = init_v_available(k, r)

if c == 1:
    chosen_col, y = find_opt_col(v_available, matrix, k, r)
    #print_ma(matrix)
    print(y + 1)

while not winner:
    adversary_col = int(input())
    adversary_col-=1
    update_v_available_matrix_oponent(matrix, v_available, adversary_col)
    chosen_col, y = find_opt_col(v_available, matrix, k, r)
    #print_ma(matrix)
    print(y + 1)