import numpy as np
import numba


@numba.jit(nopython=True)
def switch(chromosome):
    len_chromosome = len(chromosome)
    c1 = chromosome.copy()
    h = len_chromosome // 2
    r = np.random.randint(0, 2)

    c = c1[:h] if r == 0 else c1[h:]
    nonzero_indices = np.where(c != 0)[0]

    if nonzero_indices.size == 0:
        c = c1[h:] if r == 0 else c1[:h]
        nonzero_indices = np.where(c != 0)[0]

    if nonzero_indices.size <= 1:
        return c1

    r1, r2 = np.random.choice(nonzero_indices, 2, replace=False)

    c[r1], c[r2] = c[r2], c[r1]  # swap

    return c1