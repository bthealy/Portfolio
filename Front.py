import numpy as np
from copy import deepcopy


class Front:
    def __init__(self, start):
        self.prev    = {}
        self.main    = {start:None}
        self.query   = {}
        self.checked = {}
        self.last_node_visited = start

    # use after a main front has been finished
    def rotate_fronts(self):
        self.prev  = deepcopy(self.main)
        self.main  = deepcopy(self.query)
        self.query = {}

    # use after bellman iterations if another bellman will follow
    def next_bellman(self):
        self.main[self.last_node_visited] = None
        del self.checked[self.last_node_visited]

    @staticmethod
    # method to get valid neighboring positions (not obstacles or off map)
    def get_front(pos, map_features, step_size):
        left, right, top, bottom = map_features.boundary
        s = step_size

        front = [(pos[0]+s, pos[1]),
                 (pos[0]+s, pos[1]+s),
                 (pos[0],   pos[1]+s),
                 (pos[0]-s, pos[1]+s),
                 (pos[0]-s, pos[1]),
                 (pos[0]-s, pos[1]-s),
                 (pos[0],   pos[1]-s),
                 (pos[0]+s, pos[1]-s)]


        return [p for p in front if (p not in map_features.obstacles.keys()) &
                                    (p[0] > left) & (p[0] < right) &
                                    (p[1] > top)  & (p[1] < bottom)]
