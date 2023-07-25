from fix_overlap_order import shift
from copy import deepcopy
from random import randint


def mutate(chromosome, num_trucks):
    child = deepcopy(chromosome)

    s = int(len(chromosome) / num_trucks)

    # random gene
    gene = randint(0, len(child) - 1)

    # if gene already != 0, change to 0
    if child[gene] != 0:
        child[gene] = 0

        if gene < s:
            child[gene + s] = max(child) + 1
        else:
            child[gene - s] = max(child) + 1

    # if gene already = 0, change to end of visit order
    else:
        child[gene] = max(child) + 1

        if gene < s:
            child[gene + s] = 0
        else:
            child[gene - s] = 0

    # shift values per truck
    child[:s] = shift(child[:s], num_trucks)
    child[s:] = shift(child[s:], num_trucks)

    return child