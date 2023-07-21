import numpy as np
from Front import Front
get_front = Front.get_front


class Node:
    def __init__(self, position, cost=np.inf):
        self.position = position
        self.cost = cost            # cost to this position
        self.edge = None            # prev position for current path to this position

    # subprocess for each position
    def update_cost(self, cost_map, fronts, map_features, step_size):
        # front for this position
        node_front = get_front(self.position, map_features, step_size)

        # for every neighbor to this node
        for pos in node_front:
            # update query if neighbor is not part of main or prev front
            if pos not in fronts.main.keys() and \
               pos not in fronts.prev.keys() and \
               pos not in fronts.query.keys():
                fronts.query[pos] = None

            # cost from this position to neighbor
            cost = self.calculate_cost(pos, map_features.impedance)

            # if neighbor hasn't had a node initiated yet
            if pos not in cost_map.keys():
                # init neighbor node with current node as path
                cost_map[pos] = Node(pos)
                cost_map[pos].cost = cost
                cost_map[pos].edge = self.position

            # if neighbor has already been visited
            else:
                # if current node is the best path to neighbor
                if cost_map[pos].cost > cost:

                    # flag neighbor for revisit
                    fronts.query[pos] = None

                    if pos in fronts.checked.keys():
                        del fronts.checked[pos]

                    # update neighbor attributes
                    cost_map[pos].cost = cost
                    cost_map[pos].edge = self.position

        # self.position has been visited
        fronts.checked[self.position] = None

        # last node visited used to start following bellman iterations
        fronts.last_node_visited = self.position
        return cost_map

    def calculate_cost(self, pos, impedance):
        # Euclidean distance
        edge_distance = np.linalg.norm(np.array(self.position) - np.array(pos))

        # Map impedance --> elevation change, terrain roughness, etc
        imp = impedance.get((self.position, pos), impedance.get((pos, self.position), 0))

        # cost to neighbor = cost to this node + node distance + map impedance
        return self.cost + edge_distance + 0 # imp