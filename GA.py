from random import randint


class GA():
    def __init__(self):
        # Upper limit for number of convolutions
        self.conv_range = 2

        # Ranges for filter, kernel, pooling values
        self.f_range = list(range(4, 21, 2))
        self.k_range = list(range(2, 6))
        self.pool_range = [3, 4, 5]

        # Upper limit for number of dense layers
        self.d_range = 1

        # Range for layer sizes, dropout values
        self.dense_range = list(range(4, 16, 2))
        self.drop_range = [x / 100 for x in range(20, 51, 2)]

        # list to be passed for chromosome initialization
        self.range_list = [self.f_range, self.k_range, self.pool_range,
                           self.dense_range, self.drop_range]


    def init_chromosomes(self, num_c):
        c_list = []

        for _ in range(num_c):
            num_conv = randint(1, self.conv_range)

            if num_conv == 1:
                f = [self.f_range[randint(0, len(self.f_range) - 1)]]
                k = [self.k_range[randint(0, len(self.k_range) - 1)]]
                p = [self.pool_range[randint(0, len(self.pool_range) - 1)]]

            else:
                f = [self.f_range[randint(0, len(self.f_range) - 1)] for _ in range(num_conv)]
                k = [self.k_range[randint(0, len(self.k_range) - 1)] for _ in range(num_conv)]

                p = [self.pool_range[randint(0, len(self.pool_range) - 1)] for _ in range(num_conv)]

            num_dense = randint(1, self.d_range)

            if num_dense == 1:
                d = [self.dense_range[randint(0, len(self.dense_range) - 1)]]
                dr = [self.drop_range[randint(0, len(self.drop_range) - 1)]]

            else:
                d = [self.dense_range[randint(0, len(self.dense_range) - 1)] for _ in range(num_dense)]
                dr = [self.drop_range[randint(0, len(self.drop_range) - 1)] for _ in range(num_dense)]

            chromosome = [f, k, p, d, dr, 'NA']

            #             chromosome = {'filters': f,
            #                           'kernels': k,
            #                           'pool':    p,
            #                           'dense':   d,
            #                           'dropout': dr,
            #                           'fitness': 0}

            c_list.append(chromosome)

        return c_list
