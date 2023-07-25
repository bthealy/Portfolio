from GA_utils import calculate_distance
from random import randint


def update_fitness(c_list, start, num_houses, house_locations, initial=False):
    fitness = [0] * len(c_list)
    d = []
    s = num_houses
    x = pow(10, 200)

    for i in range(len(c_list)):
        fitness[i] += calculate_distance(c_list[i][:s], start[0], house_locations)
        fitness[i] += calculate_distance(c_list[i][s:], start[1], house_locations)

        d.append(fitness[i])

        fitness[i] = x / (pow(fitness[i], 100))

        if initial:
            fitness[i] *= x

    return fitness, min(d)


def update_f_ratio(fitness):
    f_total = sum(fitness)
    f_ratio = [f / f_total for f in fitness]
    return f_ratio


def roulette_wheel(f_ratio, num_to_keep, c_list):
    # create wheel
    wheel = [f_ratio[0]]

    for i in range(1, len(f_ratio) - 1):
        wheel.append(f_ratio[i] + wheel[i - 1])

    wheel.append(1)

    # spin wheel
    chromosomes_to_keep = []

    while len(chromosomes_to_keep) < num_to_keep:
        r = randint(0, pow(10, 15)) / pow(10, 15)

        for j in range(len(wheel)):
            if r <= wheel[j] and j not in chromosomes_to_keep:
                chromosomes_to_keep.append(j)
                break

    # update chromosome list
    new_generation = []

    for i in chromosomes_to_keep:
        new_generation.append(c_list[i])

    return new_generation