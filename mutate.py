from copy import deepcopy
from random import randint

def mutate(range_list, chromosome):
    # [f, k, p, d, dr, fit]

    child = deepcopy(chromosome)
    gene_idx = randint(0, len(child) - 2)

    if len(child[gene_idx]) == 1:
        child[gene_idx] = [range_list[gene_idx][randint(0, len(range_list[gene_idx]) - 1)]]

    else:
        idx = randint(0, len(child[gene_idx]) - 1)
        child[gene_idx][idx] = range_list[gene_idx][randint(0, len(range_list[gene_idx]) - 1)]

    child[-1] = 'NA'
    return child