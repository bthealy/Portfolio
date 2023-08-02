from random import randint

def roulette_wheel(c_list, f_ratio, num_to_keep):
    # create wheel
    wheel = [f_ratio[0]]

    for i in range(1, len(f_ratio) - 1):
        wheel.append(f_ratio[i] + wheel[i - 1])

    # spin wheel
    chromosomes_to_keep = []

    while len(chromosomes_to_keep) < num_to_keep:
        r = randint(0, pow(10, 3)) / pow(10, 3)

        for j in range(len(wheel)):
            if r <= wheel[j] and j not in chromosomes_to_keep:
                chromosomes_to_keep.append(j)
                break

    # update chromosome list
    new_generation = []

    for i in chromosomes_to_keep:
        new_generation.append(c_list[i])

    return new_generation