import numpy as np
from random import sample
from fix_overlap_order import fix_order
from GA_utils import distance, rotate_order
from mutate import mutate


def initialize_houses(city, start, num_houses):
    height, width = city.shape

    # Generate all possible locations
    all_locations = set((r, c) for r in range(height) for c in range(width))

    # Remove start locations from the set of all locations
    all_locations.difference_update(start)

    # Draw a random sample of locations
    locations = sample(all_locations, num_houses)

    return locations


def initialize_chromosomes(start, house_locations, num_trucks, num_chromosomes):
    num_houses = len(house_locations)

    # initialize list of chromosomes
    c_list = [np.zeros(num_houses * num_trucks) for _ in range(num_chromosomes)]

    # assign houses to genes
    dist0 = np.array([distance(start[0], house) for house in house_locations])
    dist1 = np.array([distance(start[1], house) for house in house_locations])

    new_c = np.zeros(num_houses * num_trucks)
    new_c[:num_houses] = np.where(dist0 < dist1, np.arange(num_houses), 0)
    new_c[num_houses:] = np.where(dist0 >= dist1, np.arange(num_houses), 0)

    new_c[:num_houses] = fix_order(new_c[:num_houses], 2)
    new_c[num_houses:] = fix_order(new_c[num_houses:], 2)

    c_list[0] = new_c

    for i in range(1, len(c_list)):
        # randomize new chromosome
        new_c = rotate_order(new_c)

        for _ in range(20):
            new_c = mutate(new_c, 2)

        # save chromosome to list
        c_list[i] = new_c

    return c_list
