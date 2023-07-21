import plotly.graph_objects as go
from contour_maps import get_map
from numpy import flip

def show_results(start, end, cost_map, map_features):
    # Check if there is a path from start to end
    if end in cost_map:
        # Backtrack the path from end to start
        path = []
        current = end
        while current != start:
            path.append(current)
            current = cost_map[current].edge
        path.append(start)

        # Reverse the path to get the correct order
        path.reverse()

        # Print the path
        print(start, end)
        print("Path found:")
        print(path)
        print('\ncost ', cost_map[end].cost)
        z = get_map()
        # z = flip(z, axis=0)
        plot_results(z, path, list(map_features.obstacles.keys()))

    else:
        print("No path found.")



def plot_results(z, path, obstacles):
    # Create the contour plot
    fig = go.Figure(data=go.Contour(z=z))

    # Add the path as scatter markers
    x_path, y_path = zip(*path)
    fig.add_trace(go.Scatter(x=x_path, y=y_path, mode='lines+markers', name='Path'))

    # Add obstacles as scatter markers
    x_obstacles, y_obstacles = zip(*obstacles)
    fig.add_trace(go.Scatter(x=x_obstacles, y=y_obstacles, mode='markers', name='Obstacles',
                             marker=dict(symbol='x', size=10, color='black')))

    # Set the axis labels
    fig.update_layout(xaxis_title='X', yaxis_title='Y')

    # Show the plot
    fig.show()