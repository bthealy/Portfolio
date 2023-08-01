max_depth = 990

def bellman(pos, fronts, cost_map, map_features, step_size, depth=0, stop_flag=False):
    # pos          = tuple of current position being visited
    # cost_map     = dictionary of cost for each position

    # fronts       = object containing prev, main, query fronts & checked dictionaries
    # step_size    = step size when creating front lists

    # map_features = object containing boundary, obstacles, impedance dictionaries

    # depth        = Stop recursion before limit
    # stop_flag    = ""

    # if all positions have the optimal edge, end program
    if set(map_features.all_pos).issubset(fronts.checked):
        return cost_map

    # stop recursions before limit
    elif depth >= max_depth:
        if stop_flag:
            return cost_map

    # perform subprocess
    else:
        # if main_front finished, reset fronts
        if set(fronts.main).issubset(fronts.checked):
            fronts.rotate_fronts()
            # prev  = main
            # main  = query
            # query = {}

        # for each position in main
        for p in fronts.main:

            # if point needs to be visited
            if p not in fronts.checked.keys():

                # perform subprocess
                cost_map = cost_map[p].update_cost(cost_map, fronts, map_features, step_size)

                # recursion
                bellman(pos, fronts, cost_map, map_features, step_size,
                        depth + 1, stop_flag=(depth + 1 == max_depth))

    return cost_map