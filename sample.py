from random import randint

c, g = map(int, input().split())

needed = 4
winner = False

if g == 1:
    k, r = 7, 6
elif g == 2:
    k, r = 7, 100
elif g == 3:
    k, r = 70, 10
elif g == 4:
    k, r = 140, 120
    needed = 5

if c == 1:
    chosen_col = randint(1, k)
    print(chosen_col)

while not winner:
    adversary_col = int(input())
    chosen_col = randint(1, k)
    print(chosen_col)
