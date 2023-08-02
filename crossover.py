from copy import deepcopy
from random import randint

def crossover(c1, c2):
    # how many genes to cross?
    num_genes = randint(2, 3)

    child = deepcopy(c1)

    gene_idxs = []
    # genes = [f, k, p, d, dr, fit]

    while len(gene_idxs) < num_genes:
        idx = randint(0, len(child) - 2)
        if idx not in gene_idxs:
            gene_idxs.append(idx)

    for idx in gene_idxs:
        if len(child[idx]) == len(c2[idx]):
            child[idx] = c2[idx]
        else:
            if len(child[idx]) < len(c2[idx]):
                child[idx] = c2[idx][:len(child[idx])]
            else:
                child[idx][:len(c2[idx])] = c2[idx]

    child[-1] = 'NA'
    return child