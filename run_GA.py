# %matplotlib inline # use if in notebook
from matplotlib import pyplot as plt
from random import randint
from crossover import crossover
from crossover_2 import crossover_2
from mutate import mutate
from test_chromosome import test_chromosome
from fitness import calculate_fitness_ratios
from roulette_wheel import roulette_wheel
from GA import GA


def run_GA(X, y, num_c, num_epochs, generations):
    ga = GA()
    c_list = ga.init_chromosomes(num_c)
    best_fitness = 0
    best_losses = []
    fit_ratio_history = []
    ave_loss_his = []

    for g in range(generations):
        print(f"\ngeneration: {g}")

        num_chrom = len(c_list)

        for i in range(num_chrom):
            # randomly choose genetic operator
            op = randint(0, 10) / 10.0
            cross_rate = 0.33

            # crossover chromosomes
            if op <= cross_rate:

                # choose gene 2
                c2 = c_list[randint(0, len(c_list) - 1)]
                while c2 is c_list[i]:
                    c2 = c_list[randint(0, len(c_list) - 1)]

                c_list.append(crossover_2(c_list[i], c2))

            #                     # choose type of crossover
            #                     if op <= cross_rate/2:
            #                         c_list.append(self.crossover(c_list[i], c2))
            #                     else:
            #                         c_list.append(self.crossover_2(c_list[i], c2))

            # mutate chromosome
            else:
                c_list.append(mutate(c_list[i]))

        # test chromosomes
        for i in range(len(c_list)):
            if c_list[i][-1] == 'NA':
                c_list[i][-1] = test_chromosome(c_list[i], X, y, num_epochs)

        # calculate fitness ratios
        fitness_ratios, gen_best_fitness, ave_loss, best_loss = calculate_fitness_ratios(c_list)
        ave_loss_his.append(ave_loss)
        best_losses.append(best_loss)

        # update best chrosomsome, fit history
        best_idx = fitness_ratios.index(max(fitness_ratios))
        fit_ratio_history.append(c_list[best_idx][-1])

        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_chromosome = c_list[best_idx]

        print('gen ave loss  = ', ave_loss_his[-1])
        print('gen best loss = ', best_losses[-1])

        # chromosome list w/ new generation
        # use less chromosomes as GA progresses to improve speed
        if g < generations / 4:
            c_list = roulette_wheel(c_list, fitness_ratios, num_c)
        elif g < generations / 2:
            c_list = roulette_wheel(c_list, fitness_ratios, num_c / 2)
        else:
            c_list = roulette_wheel(c_list, fitness_ratios, num_c / 4)

    # plot fitness results
    plt.plot(list(range(len(best_losses))), best_losses)
    plt.plot(list(range(len(ave_loss_his))), ave_loss_his)
    plt.legend(['Best Loss', 'Ave loss'])
    plt.ylabel('Validation Loss')
    plt.xlabel('Generation')
    plt.show()

    return best_chromosome, c_list