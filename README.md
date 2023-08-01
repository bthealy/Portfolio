# Bellman-Ford Path Planner

This project is intended to demonstrate an ability to apply dynamic and graph algorithms to robotics and intelligent systems.

The robot navigates a contour map (numpy array format) with given start, end, and obstacle coordinates. The cost for each location is a combination of Euclidean distance and impedance. Impedance is defined as the elevation change between each coordinate on the contour map, but can easily be manipulated to add cost for factors such as terrain roughness or turn radius. Additionally, limits on steepness can be set to replicate re-world traversability capabilities.

## Example paths
Example 1 <br />
<img src="Images/bellman-ford example 1.png" width="1400"> <br /><br />
Example 2 <br />
<img src="Images/bellman-ford example 2.png" width="1400"> <br /><br />
Example 3 <br />
<img src="Images/bellman-ford example 3.png" width="1400"> <br /><br />
Example 4 <br />
<img src="Images/bellman-ford example 4.png" width="1400"> <br /><br />

## Script Descriptions
run_bellman.py - Runs full process: returns path, cost, plots path on contour.<br />
bellman.py - Performs node subprocesses recursively.<br />
Node.py - Subprocess for each node in graphical algorithm. <br />
Front.py - Contains Front object which stores main front, back, and query lists.<br />
Map_Features.py - Preps contour map: initializes obstacles, impedances.<br />
Results.py - Plots results.<br />
contour_maps.py - Contains contour maps.



