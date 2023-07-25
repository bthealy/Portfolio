import numpy as np
import matplotlib.pyplot as plt
from math import sqrt



def rotate_order(c):
    h = len(c) // 2

    perm = np.random.permutation(h)
    c[:h] = c[:h][perm]

    perm = np.random.permutation(h)
    c[h:] = c[h:][perm]

    return c



def calculate_distance(chromosome, start, house_locations):
    if chromosome.any() == 0:
        return 0

    # get order of houses
    non_zero_indices = np.where(chromosome != 0)[0]
    house_order = np.argsort(chromosome[non_zero_indices]).tolist()

    # distance from start to first house
    d = 0
    h_ = house_order.index(min(house_order))
    d += distance(start, house_locations[h_])

    # distance between houses
    for h in range(1, len(house_order)):
        h_ = house_order[h]
        h_1 = house_order[h - 1]
        d += distance(house_locations[h_], house_locations[h_1])

    # distance from last house to start
    h_ = house_order.index(max(house_order))
    d += distance(start, house_locations[h_])

    return d



def distance(a, b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))



def show_map(city, house_locations, chromosome):
    m = city

    truck1 = chromosome[:len(house_locations)]
    truck2 = chromosome[len(house_locations):]

    t1 = np.where(truck1 != 0)[0]

    for i in range(len(house_locations)):
        if i in t1:
            m[house_locations[i]] = 1
        else:
            m[house_locations[i]] = 2

    m[(10, 5)] = 3
    m[(25, 30)] = 3

    plt.figure()
    plt.imshow(m)
    plt.savefig('map.png')