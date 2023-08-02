# Bellman-Ford Path Planner

Welcome to this demonstration of combining classical graph theory with robotics and intelligent systems, creating a robust path planner leveraging the Bellman-Ford algorithm. This project uses a contour map (in numpy array format) and navigates it with precise start, end, and obstacle coordinates. 

The algorithm takes into account various factors such as the Euclidean distance and impedance while deciding the cost for each node. The impedance is primarily the elevation change between each coordinate on the contour map, making this solution versatile for uneven terrains and challenging environments. This project can also incorporate factors like terrain roughness or turn radius, allowing us to simulate real-world traversal capabilities effectively. 

## Visualizing Paths

Take a peek into the workings of the Bellman-Ford path planner through these example paths. Each example provides a unique scenario showcasing the adaptability and robustness of the planner.

### Example 1
<img src="Images/bellman-ford example 1.png" width="1400"> <br /><br />

### Example 2
<img src="Images/bellman-ford example 2.png" width="1400"> <br /><br />

### Example 3
<img src="Images/bellman-ford example 3.png" width="1400"> <br /><br />

### Example 4
<img src="Images/bellman-ford example 4.png" width="1400"> <br /><br />

## Dive into the Code

### Scripts Overview

- `run_bellman.py`: This is the central script that ties the entire process together. It generates the path, calculates the cost, and plots the path on the contour.
- `bellman.py`: This script carries out the core Bellman-Ford algorithm by performing the node subprocesses recursively.
- `Node.py`: Defines each node in the graphical algorithm and contains the subprocess for each node.
- `Front.py`: This script handles the Front object that manages the main front, back, and query lists.
- `Map_Features.py`: Preps the contour map by initializing obstacles and impedances.
- `Results.py`: A script for visual delight, this plots the results of the path planner's run.
- `contour_maps.py`: This script contains the various contour maps used for path planning.

The scripts in this repository provide an insightful exploration into how classic graph algorithms can be harnessed for modern robotics and intelligent systems applications. Step in and get started with this incredible journey!
