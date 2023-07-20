#include <Arduino.h>
#include "globals.h" // Import the global variables
#include "myFunctions.h" // Import the function declarations

void setup() {
  setupHardware();
}

void loop() {
  reed_switch();
  magnetometer();
  servoControl();
  solenoidControl();
  finish();
}
