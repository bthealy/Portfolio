def calculate_fitness_ratios(c_list):
    losses = []
    fitness_ratios = []
    fitness = []

    for c in c_list:
        losses.append(c[-1])
        fitness.append(pow(1 / c[-1], 8))

    s = sum(fitness)
    best_fitness = max(fitness)
    ave_loss = sum(losses) / len(losses)
    best_loss = min(losses)

    for c in c_list:
        ratio = pow(1 / c[-1], 8) / s
        fitness_ratios.append(ratio)

    return fitness_ratios, best_fitness, ave_loss, best_loss