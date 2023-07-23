import numpy as np
from numpy import cos, sin, radians as rad
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import String
import cv2

class lidar:
    def __init__(self):
        # angle of sensors in lidar array
        self.sensor_angles = [-15, 1, -13, 3, -11, 5, -9, 7,
                              -7, 9, -5, 11, -3, 13, -1, 15]

        # vertical offset of each sensor from origin in mm
        self.vertical_offset = [11.2, -.7, 9.7, -2.2, 8.1, -3.7, 6.6, -5.1,
                                5.1, -6.6, 3.7, -8.1, 2.2, -9.7, 0.7, 11.2]

        # distances returned by each individual sensor
        self.decoded_distances = [0] * len(self.sensor_angles)

        # current lidar azimuth angle
        self.lidar_angle = 0

        # lidar rotational range
        self.angle_range = list(np.array(range(0, 36000)) / 100)

        # dictionaries to associate lidar angle with xyz distance list
        # list of num_sensor dictionaries
        self.distance_history = {}

    
    def decode_output(self, data_block):
        # raw data in hex retrieved from ROS node
        data_block = data_block.split(" ")

        # 1) Block starts after "ff ee"
        data_block.pop(0)
        data_block.pop(0)

        # 2) reverse and merge hex output for decimal conversion
        split_data = [data_block[i + 1] + data_block[i] for i in range(0, len(data_block), 2)]

        # 3) azimuth --> reverse first two columns of block,
        # combine into 1 hex, convert to dec, divide by 100
        self.lidar_angle = int(split_data[0], 16) / 100
        split_data.pop(0)

        # 4) distance --> reverse columns, combine into 1 hex,
        # convert to dec, multiply by 2mm --> gives mm
        # then add offset from vertical correction
        # correct distance is strongest output per sensor

        # separate readings by sensor
        sensor_readings = [split_data[i:len(split_data):len(self.sensor_angles)] for i in range(len(self.sensor_angles))]

        # distances decimal
        for data_list in sensor_readings:
            data_list = [int(data, 16) for data in data_list]

        # use max(), add offset, convert to m
        for s in range(len(sensor_readings)):
            max_distance = max(sensor_readings[s])
            self.decoded_distances[s] = round(((max_distance * 2 + self.vertical_offset[s]) / 1000), 4)


    def distances_to_polar_coordinates(self):
        xyz_distances = [
            [
                self.decoded_distances[i] * cos(rad(self.sensor_angles[i])) * cos(rad(self.lidar_angle)),
                self.decoded_distances[i] * cos(rad(self.sensor_angles[i])) * sin(rad(self.lidar_angle)),
                self.decoded_distances[i] * sin(rad(self.sensor_angles[i]))
            ]
            for i in range(len(self.sensor_angles))
        ]

        # update dictionary with xyz distances
        self.distance_history[f"{self.lidar_angle}"] = xyz_distances


    def polar_to_cartesian(self, polar_points):
        cartesian_points = []
        for distance, angle in polar_points:
            x = distance * np.cos(np.radians(angle))
            y = distance * np.sin(np.radians(angle))
            cartesian_points.append((x, y))
        return cartesian_points


    # %% Set ROS nodes, topics, rate
    def ROS_set(self, sub_node, sub_topic, pub_node=None, pub_topic=None, rate=10):
        self.sub_node = sub_node
        self.sub_topic = sub_topic
        self.pub_node = pub_node
        self.pub_topic = pub_topic
        self.pub_rate = rate

    # %% ROS subscriber --> subscribe to node outputting raw hex data
    def ROS_callback(data):
        global data_block
        data_block = data

    def ROS_retrieve_data(self):
        rospy.init_node(self.sub_node)
        rospy.Subscriber(self.sub_topic, String, self.ROS_callback)
        rospy.spin()

    # %% ROS Publisher --> publish coordinates, edge points, etc
    def ROS_create_publisher(self):
        self.pub = rospy.Publisher(self.pub_topic, String, queue_size=10)
        rospy.init_node(self.pub_node)
        self.r = rospy.Rate(self.rate)  # 10hz


    # %% Full process (excluding plot)
    def full_process(self):
        while True:
            # retrieve raw data using ROS subscriber
            self.ROS_retrieve_data()

            # process data
            self.decode_output()
            self.distances_to_polar_coordinates()

            # publish coordinates, edges, etc. to ROS
            self.pub.publish(f"{self.distance_history}")
            self.r.sleep()


    # %% Edge detection
    def edge_detection(self, polar_points, threshold1=50, threshold2=150):
        # Convert polar coordinates to Cartesian coordinates
        cartesian_points = self.polar_to_cartesian(polar_points)

        # Create an empty black image to represent the point cloud
        max_x = max(cartesian_points, key=lambda point: point[0])[0]
        max_y = max(cartesian_points, key=lambda point: point[1])[1]
        min_x = min(cartesian_points, key=lambda point: point[0])[0]
        min_y = min(cartesian_points, key=lambda point: point[1])[1]
        width = int(max_x - min_x) + 1
        height = int(max_y - min_y) + 1
        image = np.zeros((height, width), dtype=np.uint8)

        # Shift points to non-negative coordinates to fit the image
        shifted_points = [(int(point[0] - min_x), int(point[1] - min_y)) for point in cartesian_points]

        # Draw the points on the image
        for point in shifted_points:
            x, y = point
            image[y, x] = 255

        # Apply Canny edge detection
        edges = cv2.Canny(image, threshold1, threshold2)

        # Find the coordinates of the edge points in Cartesian coordinates
        edge_points_cartesian = []
        for y in range(height):
            for x in range(width):
                if edges[y, x] == 255:
                    edge_points_cartesian.append((x + min_x, y + min_y))

        # Convert the Cartesian edge points back to polar coordinates
        edge_points_polar = []
        for x, y in edge_points_cartesian:
            distance = np.sqrt(x ** 2 + y ** 2)
            angle = np.degrees(np.arctan2(y, x))
            edge_points_polar.append((distance, angle))

        return edge_points_polar


    # %% Plot point cloud
    def plot_coordinates(self, angle_range=[0, 360], density=1):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        x, y, z = ([],[],[])

        angles = list(np.array(range(angle_range[0] * 100, angle_range[1] * 100)) / 100)
        angles = angles[::density]

        for angle in angles:
            for sensor in self.distance_history[f"{angle}"]:
                x.append(sensor[0])
                y.append(sensor[1])
                z.append(sensor[2])

        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.set_zlim(min(z), max(z))

        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')

        ax.scatter3D(x, y, z)
        plt.show()


    # %% create data to test plot
    def create_test_data(self):
        # for angle in lidar rotational range
        for angle in self.angle_range:
            self.lidar_angle = angle

            xyz_distances = []

            # for each sensor in array
            for s in range(len(self.sensor_angles)):
                d = 5

                dz = d * sin(rad(self.sensor_angles[s]))

                dx_dy = d * cos(rad(self.sensor_angles[s]))

                dx = dx_dy * cos(rad(self.lidar_angle))
                dy = dx_dy * sin(rad(self.lidar_angle))

                xyz_distances.append([dx, dy, dz])

            # append list of sensor distances to dictionary of rotation angles
            self.distance_history[f"{self.lidar_angle}"] = (xyz_distances)


# %% example of plot
lidar = lidar()
lidar.create_test_data()
lidar.plot_coordinates(angle_range=[0, 360], density=150)
