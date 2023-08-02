# Velodyne Lidar Real-Time Processing for Django Robot

Welcome to this repository. Here you will find robust, tested code developed to handle the data output from a Velodyne Lidar system, a professional-grade lidar used in a range of applications, including autonomous vehicles and robotics. The code was specifically designed for use on a real-time Django robot.

## System Overview

The provided Python script aims to simplify and streamline the process of interacting with raw data output from a Velodyne Lidar system. By subscribing to a relevant ROS node, the script decodes this data and then converts it into more utilizable formats—polar and cartesian coordinates. 

This repository also includes a data interpretation layer that uses the CV2 Canny edge detection algorithm to identify boundaries in the robot's environment. After processing, the data, including coordinates and detected edges, is published to a ROS node for further use.

Additionally, the script offers data visualization using Matplotlib, providing an interactive 3D graph. This feature enables a user-friendly way to analyze the lidar data, facilitating debugging and optimization processes.

## Code Breakdown

The core components of the code are categorized as follows:

1. **Lidar Class Initialization:** This segment establishes the Lidar class and initializes critical parameters such as sensor angles, vertical offset, decoded distances, and the lidar's rotational range. It also sets up the dictionary to capture the history of distances for each lidar angle.

2. **Data Decoding:** This segment manages the decoding of the raw data harvested from the Velodyne Lidar through the ROS node. It processes the azimuth and distance readings and applies vertical corrections to the sensor readings.

3. **Coordinate Transformations:** The processed data is converted from decoded distances to polar coordinates and stored within the distance history dictionary. The segment also incorporates a function for the transformation of polar coordinates to cartesian coordinates.

4. **ROS Communications:** This set of functions oversees the ROS interfacing, establishing the subscriber and publisher nodes and topics, retrieving raw data from the specified ROS topic, and publishing the decoded data.

5. **Edge Detection:** Using the CV2 Canny edge detection algorithm, this function identifies environmental edges from the polar coordinate inputs. After the conversion of these points to cartesian coordinates, the edge detection process is applied, and the edge points are returned in polar coordinates.

6. **Data Visualization:** This function creates a 3D visualization of the points using Matplotlib, providing an easy-to-interpret representation of the lidar data.

7. **Test Data Generation:** The code also includes a function for generating test data for visualization purposes.

The final portion of the code gives an example of using the lidar class by generating test data and rendering it.
