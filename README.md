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

- `run_bellman.py`: This is the central script that ties the entire process together. It generates the path, calculates the cost, and plots the path on the contour. <br />
- `bellman.py`: This script carries out the core Bellman-Ford algorithm by performing the node subprocesses recursively.<br />
- `Node.py`: Defines each node in the graphical algorithm and contains the subprocess for each node.<br />
- `Front.py`: This script handles the Front object that manages the main front, back, and query lists.<br />
- `Map_Features.py`: Preps the contour map by initializing obstacles and impedances.<br />
- `Results.py`: A script for visual delight, this plots the results of the path planner's run.<br />
- `contour_maps.py`: This script contains the various contour maps used for path planning.


## Reflections and Learnings

The development process of this project was not without its hurdles. Two challenges, in particular, stood out:

1) Achieving a balance between the Euclidean distance and elevation impedance cost was quite a juggling act. The path chosen by the algorithm could be significantly influenced by the penalty associated with elevation. It took a fair amount of experimentation to strike an optimal balance, as overemphasizing one type of cost would lead to the other being overlooked.
   
2) The current design uses only elevation change to calculate impedance, leading to scenarios where paths of the same Euclidean distance but varying steepness were treated the same. While the algorithm was able to reduce overall elevation change, it did not necessarily prioritize less-steep paths.

A practical solution to these problems would be to incorporate real contours and robotic limitations. Having real-world constraints on the vehicle's traversal capabilities would provide a more concrete framework for adjusting the cost function and balancing Euclidean distance and elevation impedance.
