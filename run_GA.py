import numpy as np
from GA import run_GA
from intialize_GA import initialize_houses

# ratio = crossover, switch, mutate
# cross  ratio = ratio[0]
# switch ratio = ratio[1] - ratio[0]
# mutate ratio = 1 - ratio[1]
ratio = [0, 0.8]

gen   = 800 # number of generations
num_c = 10  # number of chromosomes
num_h = 50  # number of houses
#NOTE num_c < num_h / 2

start = [(10, 5), (25, 30)]
city = np.zeros((35, 35))
house_locations = initialize_houses(city, start, num_h)

chromosome, distance = run_GA(city, start, house_locations, gen, num_c, ratio)