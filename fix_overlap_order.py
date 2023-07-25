from random import randint
import numpy as np
import numba

@numba.jit(nopython=True)
def fix_order(child, num_trucks):
    # if a truck has 2 of the same values, change one
    check = list(child)
    repeated_num = []

    for i in range(1, len(check) + 1):
        count = check.count(i)
        if count > 1:
            repeated_num.append(i)

    if len(repeated_num) > 0:
        # move repeated numbers to end of order
        for n in repeated_num:
            row = np.where(child == n)[0]
            r = randint(0, len(row) - 1)
            child[row[r]] = max(child) + 1

    child = shift(child, num_trucks)

    return child



def fix_overlap(child, multiple_trucks, no_trucks, num_trucks, s):
    m = max(child)

    # randomly choose which truck loses or gains house
    for h in multiple_trucks:
        r = randint(0, num_trucks - 1)
        child[h + s * r] = 0

    for h in no_trucks:
        r = randint(0, num_trucks - 1)
        child[h + s * r] = m + 1

    return np.array(child)


@numba.jit(nopython=True)
def shift(chromosome, num_trucks):
    c = chromosome.copy()

    b = c.argsort()

    for i in range(1, len(b)):
        while c[b[i]] - c[b[i - 1]] > 1:
            c[b[i]] -= 1

    while 1 not in c:
        if np.any(c <= 0):
            break

        c -= 1

    negative_indeces = np.where(c < 0)
    c[negative_indeces] = 0

    return c