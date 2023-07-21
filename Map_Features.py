import numpy as np
import itertools

class Map_Features:
    def __init__(self, start, end, contour, num_obstacles):
        self.alpha_imp = 2
        self.init_map(start, end, contour, num_obstacles)

    def init_map(self, start, end, contour, num_obstacles):
        # boundary for efficiency
        p = 0 # edge padding
        bottom, right = contour.shape
        self.boundary = (-1, right + p, -1, bottom + p)

        # initialize random obstacles
        self.obstacles = {}
        while len(self.obstacles) < num_obstacles:
            x = np.random.randint(self.boundary[0], self.boundary[1], num_obstacles)[0]
            y = np.random.randint(self.boundary[2], self.boundary[3], num_obstacles)[0]
            position = (x, y)

            # if p not already an obstacle, start, end:
            if position != start and position != end and position not in self.obstacles.keys():
                # create key in obstacles dic for p
                self.obstacles[position] = None

        self.get_all_pos()
        self.init_impedance(contour)

    def get_all_pos(self):
        left, right, top, bottom = self.boundary
        self.all_pos = {(i, j): None for i in range(left, right + 1)
                                     for j in range(top, bottom + 1)
                                         if (i,j) not in self.obstacles.keys()}

    def init_impedance(self, contour):
        # impedance = delta(height) between points
        # self.impedance = {}

        for pos1, pos2 in itertools.combinations(self.all_pos.keys(), 2):
            if not bool(self.impedance.get((pos1, pos2))) and not bool(self.impedance.get((pos2, pos1))):
                try: self.impedance[(pos1, pos2)] = abs(contour[pos1] - contour[pos2]) * self.alpha_imp
                except: pass
