# Embedded Velodyne Lidar Decoder / Edge Detector
This code was embedded on a Django robot to decode and interpret the raw data output from a Velodyne lidar.

The code:
1) Subscribes to the raw lidar output ROS node
2) Decodes raw lidar output
3) Converts decoded data to polar and cartesian coordinates
4) Detects edges using CV2 Canny edge detection
5) Publishes coordinates and edge locations to ROS node
6) Creates 3D graph using Matplotlib
