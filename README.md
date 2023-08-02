# Autonomous Vehicle
Welcome to our autonomous vehicle project. This repository contains a straightforward, yet engaging project that we undertook as part of an undergraduate introductory course in Robotics. Our aim was to build a simple autonomous vehicle capable of traveling a specified distance along a straight path and successfully navigating within set boundaries using magnetometer headings.

For a closer look at the project and to see our autonomous vehicle in action, feel free to check out our demonstration video via the link provided below:

## Demonstration:
https://drive.google.com/file/d/1cdRi_YOMGCwp0VcparbAZbSs_ZBniHbV/view?usp=drive_link

## Robotic System Components
**Microcontroller**
The brain of our autonomous vehicle is an Arduino microcontroller, a versatile and easy-to-program platform that effectively controls all components and processes in real-time.

**Steering**
The vehicle is equipped with a sophisticated parallel steering mechanism. This system is actuated by a servo motor, controlled via a Proportional-Integral-Derivative (PID) controller, which ensures precision and stability during the vehicle's directional changes.

**Propulsion**
For the vehicle's propulsion, we have innovatively utilized a pneumatic cylinder coupled with a solenoid valve. This combination not only provides robust power for movement but also ensures efficient energy usage by the robot.

**Direction Tracking**
The autonomous vehicle's course navigation and tracking is handled by a magnetometer heading system. The magnetometer operates like a compass, providing highly accurate real-time orientation data, thereby enabling the vehicle to stay on the right path consistently.

**Distance / Velocity Tracking**
The distance covered by the robot is meticulously tracked using a reed switch mechanism. This setup keeps a count of the number of wheel rotations, which in turn helps in calculating the accurate distance travelled by the vehicle. By comparing distance with respect to time, it was possible to track vehicle velocity.
