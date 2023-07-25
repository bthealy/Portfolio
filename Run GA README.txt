To run GA, execute the run_GA.py file.

It calls the GA_Library, then runs the GA with the preset parameters.
Set the parameters for testing different combinations.

Output prints GA time, best distance, best chromosome, then saves the
distance per gen graph and an image of the final map split among the trucks.


NOTES:
1) Algorithm sometimes get stuck if the number_chromosomes >= number_houses/2.
2) Operation ratio is set as described in code comments


## CODE INSIDE RUN_GA.PY

import numpy as np
from GA_library import run_GA, initialize_houses

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
