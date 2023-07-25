import numpy as np
from copy import deepcopy
from random import randint

def switch(chromosome):
    c1 = deepcopy(chromosome)

    h = int(len(c1) / 2)
    r = randint(0, 1)
    if r == 0:
        c = c1[:h]
        if len(np.where(c != 0)[0]) == 0:
            c = c1[h:]
    else:
        c = c1[h:]
        if len(np.where(c != 0)[0]) == 0:
            c = c1[:h]

    if len(np.where(c != 0)[0]) == 1:
        return c1

    r1 = np.random.choice(np.where(c != 0)[0], 1)

    g1 = c[r1]

    r2 = np.random.choice(np.where(c != 0)[0], 1)
    while r2 == r1:
        r2 = np.random.choice(np.where(c != 0)[0], 1)

    g2 = c[r2]

    c[r1] = g2
    c[r2] = g1

    if r == 0:
        c1[:h] = c
    else:
        c1[h:] = c

    return c1