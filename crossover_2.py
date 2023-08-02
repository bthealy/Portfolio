from copy import deepcopy
from random import randint

def crossover_2(c1, c2):
    child = deepcopy(c1)
    #     = [f, k, p, d, dr, fit]

    if randint(0, 1):
        child[:3] = c2[:3]
    else:
        child[3:5] = c2[3:5]

    child[-1] = 'NA'
    return child