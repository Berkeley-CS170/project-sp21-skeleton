import random
import sys

def generate(size, density):
    graphsize = int(size)
    contain, degree, result = set(), [], []
    for i in range(graphsize):
        for j in range(graphsize):
            if i != j and (j,i) not in contain and random.random() > (1 - float(density)):
                contain.add((i,j))
                degree.append(i)
                degree.append(j)
                result.append(str(i) + " " + str(j) + " " + str(round(random.uniform(1,99), 1)))
    test = False
    for i in range(graphsize):
        if degree.count(i) < 2:
            test = True
    return generate(size, density) if test else result

if len(sys.argv) != 3:
    print("Bad Input, please enter size (integer) and density (float 0-1)")
else:
    size, density = sys.argv[1], sys.argv[2]
    f = open(size + ".in", "w")
    try:
        for i in generate(sys.argv[1], sys.argv[2]):
            f.write(i + "\n")
    except:
        print("Bad Input, please enter size (integer) and density (float 0-1)")
