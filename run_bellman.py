import numpy as np
from bellman import bellman
from Front import Front
from Node import Node
from Map_Features import Map_Features
from Results import show_results
import time
from random import randint
from contour_maps import get_map


def run_bellman(map_id=0, num_obstacles=0, step_size=1, iteration_max=30):
    # contour map
    if map_id:
        contour = get_map(map_id)
    else:
        contour = np.zeros(shape=(100, 100))

    # normalize map
    contour = np.interp(contour, (contour.min(), contour.max()), (0, 1))

    # Define start and end positions
    start = (0, 0)
    end   = (randint(5, contour.shape[1]),
             randint(5, contour.shape[0]))

    # init boundary, obstacles, impedance
    map_features = Map_Features(start, end, contour, num_obstacles=num_obstacles, alpha_imp=100)
    # initialize cost_map with start node
    cost_map = {start: Node(start, cost=0)}

    # init front object
    fronts = Front(start)

    # Run the Bellman-Ford algorithm
    iteration_flag = 1
    t1 = time.time()

    # run multiple bellman-ford iterations if recursion limit exceeded
    while not set(map_features.all_pos).issubset(fronts.checked):
        print("iteration ", iteration_flag)

        cost_map = bellman(fronts.last_node_visited, fronts, cost_map, map_features, step_size)
        fronts.next_bellman()

        iteration_flag += 1
        if iteration_flag == iteration_max: break

    t2 = time.time()

    # Results
    show_results(start, end, cost_map, map_features, map_id)
    print("time: ", t2 - t1, " seconds")


if __name__ == "__main__":
    run_bellman(map_id=5, num_obstacles=150)