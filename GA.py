from random import randint
import matplotlib.pyplot as plt
import time
from fitness_roulette import update_fitness, update_f_ratio, roulette_wheel
from intialize_GA import initialize_chromosomes
from crossover import crossover
from mutate import mutate
from switch import switch
from GA_utils import show_map


def run_GA(city, start, house_locations, gen, num_chromosomes, ratio=[0, 0.8]):
    h = len(house_locations)
    
    c_list    = initialize_chromosomes(start, house_locations, 2, num_chromosomes+10)
    fitness, d = update_fitness(c_list, start, h, house_locations, initial=True)
    f_ratio    = update_f_ratio(fitness)

    best_fitness = []
    best_d       = []

    cross_ratio  = ratio[0]
    switch_ratio = ratio[1]

    s = len(house_locations)
    lowest_d = pow(10, 30)

    t = time.time()
    
    # start GA
    for g in range(gen):
        for i in range(len(c_list)):
            c1 = i
            c2 = randint(0, len(c_list)-1)
            
            while c1 == c2:
                c2 = randint(0, len(c_list)-1)
            
            # choose operator
            operator = randint(0, 100)/100

            if operator < cross_ratio:
                c_list.append(crossover(c_list[c1], c_list[c2], 2))
            
            elif operator < switch_ratio:
                c_list.append(switch(c_list[c1]))
            
            else:
                c_list.append(mutate(c_list[c1], 2))
        
        # evaluate chromosome
        fitness, d = update_fitness(c_list, start, s, house_locations)
        f_ratio = update_f_ratio(fitness)
        
        best_fitness.append(max(fitness))
        best_d.append(d)
        
        if d < lowest_d:
            lowest_d = d
            best_c   = c_list[fitness.index(min(fitness))] 
            
        # update chromosome list for next generation
        c_list  = roulette_wheel(f_ratio, num_chromosomes, c_list)

    print('\n\nGA time = ', time.time()-t)    
    print('\n lowest distance = ', lowest_d)
    print('\n best chromosome = ', best_c)
    
    plt.plot(best_d, label='best distance')
    plt.savefig('fitness_graph.png')
    plt.legend()
    plt.show()
    
    show_map(city, house_locations, best_c)

    return lowest_d, best_c
