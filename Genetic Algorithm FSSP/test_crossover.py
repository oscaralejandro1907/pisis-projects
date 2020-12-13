import numpy as np
import random

n=5

population=[[0, 4, 1, 2, 3], [0, 1, 2, 4, 3], [4, 1, 2, 0, 3], [1,0,4,3,2]]
parents=[[1, 3], [0, 1], [3, 2], [0, 3]]

################################################################
#for p in parents:
    #print(population[p[0]])

################################################################
def crossover(parents):
    points = list(np.random.permutation(np.arange(n-1)+1)[:2])

    if points[0] > points[1]:
        points[0], points[1] = points[1], points[0]

    print(points)

    child = list(population[0])
    print("This is the first parent:",child)

    for i in range(points[0],points[1]):
        child[i]=-1

    print("This is the child",child)
    print("This is the other parent",population[1])

    p = -1
    for i in range(points[0],points[1]):
        while True:
            p += 1
            if population[1][p] not in child:
                child[i] = population[1][p]
                break

    return child

cross_result=crossover([population[0],population[1]])
print(cross_result)