import numpy as np
from random import randint
from copy import deepcopy
from fix_overlap_order import fix_overlap, fix_order


def crossover(c1, c2, num_trucks):
    child = np.zeros(len(c1))

    num_houses = int(len(c1) / 2)

    split_i = randint(1, num_houses - 1)

    c1_t1 = deepcopy(c1[:num_houses])
    c1_t2 = deepcopy(c1[num_houses:])

    c2_t1 = deepcopy(c2[:num_houses])
    c2_t2 = deepcopy(c2[num_houses:])

    c1_t1[split_i:] = c2_t1[split_i:]
    c1_t2[split_i:] = c2_t2[split_i:]

    child = np.hstack((c1_t1, c1_t2))

    # check if only 1 non-zero per column
    # split into matrix, each a column per house
    s = num_houses
    split_child = []

    for i in range(0, num_trucks):
        split_child.append(child[s * i:s * (i + 1)])

    for i in range(0, num_trucks - 1):
        stack = np.vstack((split_child[i], split_child[i + 1]))

    # check columns
    no_trucks = []
    multiple_trucks = []

    for col in range(0, stack.shape[1]):
        non_zeros = np.where(stack[:, col] != 0)[0]

        # if not, mark houses with overlap or no trucks
        if len(non_zeros) > 1:
            multiple_trucks.append(col)

        elif len(non_zeros) == 0:
            no_trucks.append(col)

    # if a truck has overlapping values from crossover,
    # move one to back of order

    child[:s] = fix_order(child[:s], 2)
    child[s:] = fix_order(child[s:], 2)

    # if valid chromosome, return
    if len(multiple_trucks) == 0 and len(no_trucks) == 0:
        return child

    # if not valid
    child = fix_overlap(child, multiple_trucks, no_trucks, num_trucks, s)

    child[:s] = fix_order(child[:s], 2)
    child[s:] = fix_order(child[s:], 2)

    return child