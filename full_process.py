from run_GA import run_GA
from prep_data import load_data
import numpy as np

data = load_data(dir, 'processed_data')
X, y = zip(*data)

X = np.array(X)
y = np.array(y)

num_chromosomes = 10
epochs = 30
generations = 100

best_chromosome, c_list = run_GA(num_chromosomes, epochs, generations)