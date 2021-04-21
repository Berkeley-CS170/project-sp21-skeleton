import random as r

for i in range(45):
    for j in range(i + 1, 45):
        print(i, j, r.randint(1, 99))