// globals.cpp
#include "globals.h"

// Define the external variables here
float d = 2.4;
float circ = (PI * d) / 3;
int solenoidPin = 2;
int switchPin = 4;
int servoPin = 3;
int SwitchState;
int previousSwitchState = 0;
bool solenoidState = LOW;
const long interval_1 = 200;
const long interval_2 = 275;
float distanceTraveled = 0;
unsigned long previousTime = 0;
int startingPos = 89;
int servoDir = 0;
unsigned long filterHeading;
unsigned long previousFilterHeading;
float a = 0.4;
