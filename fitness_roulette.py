from GA_utils import calculate_distance
import numpy as np
import bisect


def update_fitness(c_list, start, num_houses, house_locations, initial=False):
    s = num_houses
    pow10_200 = pow(10, 200)  # compute this value once

    fitness = [calculate_distance(c[:s], start[0], house_locations) +
               calculate_distance(c[s:], start[1], house_locations)
               for c in c_list]

    d = fitness.copy()
    fitness = [pow10_200 / (pow(f, 100)) * (pow10_200 if initial else 1) for f in fitness]

    return fitness, min(d)


def update_f_ratio(fitness):
    f_total = sum(fitness)
    f_ratio = [f / f_total for f in fitness]
    return f_ratio



def roulette_wheel(f_ratio, num_to_keep, c_list):
    # create wheel
    wheel = np.cumsum(f_ratio).tolist()
    wheel[-1] = 1.0

    # spin wheel
    random_nums = [np.random.rand() for _ in range(num_to_keep)]
    chromosomes_to_keep = [bisect.bisect(wheel, r) for r in random_nums]

    # ensure chromosomes_to_keep has unique indices
    chromosomes_to_keep = list(set(chromosomes_to_keep))
    while len(chromosomes_to_keep) < num_to_keep:
        chromosomes_to_keep.append(bisect.bisect(wheel, np.random.rand()))
        chromosomes_to_keep = list(set(chromosomes_to_keep))

    # update chromosome list
    new_generation = [c_list[i] for i in chromosomes_to_keep]

    return new_generation