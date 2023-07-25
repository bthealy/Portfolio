import numpy as np
from random import randint
from fix_overlap_order import fix_order
from GA_utils import distance, rotate_order
from mutate import mutate
from copy import deepcopy


def initialize_houses(city, start, num_houses):
    locations = []
    height, width = city.shape
    houses_initialized = 0

    while houses_initialized < num_houses:
        row = randint(0, height - 1)
        col = randint(0, width - 1)

        if (row, col) not in locations and (row, col) not in start:
            locations.append((row, col))
            houses_initialized += 1

    return locations


def initialize_chromosomes(start, house_locations, num_trucks, num_chromosomes):
    c_list = []
    num_houses = len(house_locations)

    # initialize list of chromosomes
    c_list = [[0] * (num_houses * num_trucks) for _ in range(num_chromosomes)]

    # assign houses to genes
    new_c = np.zeros(num_houses * num_trucks)

    for i in range(num_houses):
        if distance(start[0], house_locations[i]) < distance(start[1], house_locations[i]):
            new_c[i] = i
        else:
            new_c[i + num_houses] = i

    new_c[:num_houses] = fix_order(new_c[:num_houses], 2)
    new_c[num_houses:] = fix_order(new_c[num_houses:], 2)

    c_list[0] = deepcopy(new_c)

    for i in range(1, len(c_list)):
        # randomize new chromosome
        new_c = rotate_order(new_c)

        for _ in range(50):
            new_c = mutate(new_c, 2)

        # save chromosome to list
        c_list[i] = deepcopy(new_c)

    return c_list
