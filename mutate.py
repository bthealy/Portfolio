from fix_overlap_order import shift
import numpy as np
import numba


@numba.jit(nopython=True)
def mutate(chromosome, num_trucks):
    len_chromosome = len(chromosome)
    child = chromosome.copy()

    s = len_chromosome // num_trucks

    # random gene
    gene = np.random.randint(0, len_chromosome)

    max_child = np.max(child) + 1

    # if gene already != 0, change to 0, otherwise change to max_child
    new_value, other_value = (0, max_child) if child[gene] != 0 else (max_child, 0)

    child[gene] = new_value

    if gene < s:
        child[gene + s] = other_value
    else:
        child[gene - s] = other_value

    # shift values per truck
    child[:s] = shift(child[:s], num_trucks)
    child[s:] = shift(child[s:], num_trucks)

    return child