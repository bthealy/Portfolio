#ifndef GLOBALS_H
#define GLOBALS_H

#include <LSM303.h>
#include <Servo.h>
#include <Wire.h>

extern LSM303 compass;
extern Servo myservo;

extern const float d;
extern const float circ;
extern const uint8_t solenoidPin;
extern const uint8_t switchPin;
extern const uint8_t servoPin;
extern const long interval_1;
extern const long interval_2;
extern const int startingPos;
extern const uint8_t a;
extern int desired_angle;

#endif // GLOBALS_H
