# Bellman-Ford Path Planner

This project is intended to demonstrate an ability to apply dynamic and graph algorithms to robotics and intelligent systems.

The robot navigates a contour map (numpy array format) with given start, end, and obstacle coordinates. The cost for each node is a combination of Euclidean distance and impedance. Impedance is set as the elevation change between each coordinate on the contour map, but can easily be manipulated to add cost for factors such as terrain roughness.

## Example paths
Example 1 <br />
<img src="Images/bellman-ford example 1.png" width="400"> <br /><br />
Example 2 <br />
<img src="Images/bellman-ford example 2.png" width="400"> <br /><br />
Example 3 <br />
<img src="Images/bellman-ford example 3.png" width="400"> <br /><br />
Example 4 <br />
<img src="Images/bellman-ford example 4.png" width="400"> <br /><br />

