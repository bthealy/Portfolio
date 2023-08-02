# Genetic Algorithm Neural Network Optimizer
This library uses a genetic algorithm to optimize the architecture and hyperparameters of CNNs. It can be manipulated to optimize any type of architecture, for example a DNN consisting of only dense layers. The current algorithm design optimizes the number of convolutional and pooling layers and each layers's individual filter, kernel, and pooling values. It then optimizes the following dense layers by choosing the number of dense and dropout layers and optimizing each layer's number of neurons and drop out values.

## Genetic Algorithms
Genetic algorithms (GAs) are a class of optimization algorithms inspired by the natural process of biological evolution. They approach problem-solving in a way that mimics the survival of the fittest among string structures, which represent potential solutions. Here is a simplified overview of how GAs solve problems:

1. **Initialization:** GAs start with a randomly generated population of candidate solutions. Each individual solution, often encoded as a binary string or array, represents a possible solution to the problem.

2. **Fitness Evaluation:** Each solution's effectiveness, or "fitness," is evaluated using a predefined fitness function, specific to the problem at hand. Higher fitness scores correlate with better solutions.

3. **Selection:** The GA then selects solutions from the current population to breed a new generation. Individuals with better fitness scores have a higher chance of being chosen. This selection process models the survival of the fittest.

4. **Crossover (Breeding):** Selected solutions are paired, and "crossover" operations are performed to produce new offspring. Crossover might involve swapping parts of two parent solutions, resulting in offspring that carry characteristics from both parents. This simulates biological reproduction and recombination.

5. **Mutation:** Random changes are introduced in the new generation through mutation, which helps to maintain diversity in the population and prevents premature convergence to sub-optimal solutions. This step is akin to genetic mutation in nature.

6. **Iteration:** Steps 2 to 5 are repeated over multiple generations, gradually evolving the population towards optimal or near-optimal solutions.

7. **Termination:** The algorithm ends when a stopping criterion is met, which could be finding a satisfactory solution, reaching a maximum number of generations, or the fitness level plateauing over generations.

Through these steps, GAs navigate the solution space, simultaneously exploiting good solutions found (exploration) and fine-tuning these solutions (exploitation), thereby mimicking the evolutionary process of nature. This unique approach makes GAs robust and versatile for solving complex optimization problems where the search space is large and solution landscapes are complex.

## Chromosomes
**Chromosome Design**:
Chromosomes contain genes, which are the individual values for each detail of the problem we are trying to solve. In this case, chromosomes are designed as followed:

chromosome = [f, k, p, d, dr, fitness]

Genes:
f - list of filter values for each convolution
k - list of kernel values for each convolution
p - list of pooling values for each pooling layer
d - list of number of neurons in each dense layer
dr - list of dropout values for each dropout layer
fitness - best validation loss for this chromosome's architecture (outliers removed)

Each gene is initialized to be a random length within a specified range. For example, if we want there to be up to 5 convolutional layers, each f will be a list of filter values that is no greater than 5 (and k will be that same length). Chromosomes will vary in their length of f and k, causing the number of convolutions to differ for each chromosome. This allows the algorithm to optimize both architecture and hyperparameter values.

## R&D
Overall, this approach is quite straight forward. The 2 issues that required attention were:

 1) Removing outliers from validation loss's. When testing each architecture, if one epoch happen to do inconsistently well on a particular validation batch, this would make the GA think this chromosome is good (even if every other epoch's val loss was terrible). To fix this, I smoothed each graph using a digital filter. This smoothing solved the issue.

 2) Overfitting. I noticed a strange phenomenon, the GA's final chromosomes were always doing notably better on the validation losses than training losses. This is obviously a red flag, and it turns out the GA would select architectures / hyperparameter combinations that weren't overall better, they just did well on a particular validation set. Ideally, validation loss per epoch should be slightly worse than training loss; indicating that the model is learning properly. To fix this, I had to penalize chromosomes' fitnesses when they had higher validation losses than training losses.
