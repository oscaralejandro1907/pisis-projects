import numpy as np
import random

n=5

hijo=[0, 4, 1, 2, 3]

def mutation(child):
    points = list(np.random.permutation(np.arange(n))[:2])

    if points[0] > points[1]:
        points[0], points[1] = points[1], points[0]

    movedJob = child[points[1]]

    for i in range(points[1], points[0], -1):
        child[i] = child[i-1]

    child[points[0]] = movedJob

    return child

sol=mutation(hijo)
print(sol)