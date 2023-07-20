#include "myFunctions.h"
#include "globals.h" // Import the global variables

void setupHardware() {
  myservo.attach(servoPin);
  pinMode(solenoidPin, OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
  compass.m_min = (LSM303::vector<int16_t>){-1949, -4200, +12589};
  compass.m_max = (LSM303::vector<int16_t>){-1471, -3275, +12884};
  myservo.write(startingPos);
}

// Inline small functions for performance improvement
inline uint8_t fastDigitalRead(uint8_t pin) {
  return (uint8_t)digitalRead(pin);
}

void reed_switch() {
  static uint8_t previousSwitchState = 0; // Move to a static local variable
  uint8_t SwitchState = fastDigitalRead(switchPin); // Use a local variable instead

  if (previousSwitchState != SwitchState) {
    if (SwitchState == 0) { // magnet has been detected
      distanceTraveled += circ;
      Serial.print("Distance Traveled (ft): ");
      Serial.println(distanceTraveled / 12); // distance traveled in ft
    }
    previousSwitchState = SwitchState;
  }
}

void magnetometer() {
  compass.read();
  uint16_t heading = compass.heading();
  uint16_t filterHeading = (a * heading + (100 - a) * previousFilterHeading) / 100; // Use a local variable
  previousFilterHeading = filterHeading; // Update the global variable
}

void servoControl() {
  static unsigned long lastPidTime = 0;
  unsigned long currentTime = millis();

  if (currentTime - lastPidTime >= pidInterval) {
    lastPidTime = currentTime;

    // Calculate error
    int headingError = desired_angle - filterHeading;

    // Proportional component
    float pidP = Kp * headingError;

    // Integral component
    pidErrorSum += Ki * headingError;
    float pidI = constrain(pidErrorSum, -50, 50);

    // Derivative component
    float pidD = Kd * (headingError - lastPidError);
    lastPidError = headingError;

    // Calculate control effort
    float controlEffort = pidP + pidI + pidD;

    // Calculate new servo position
    int newServoDir = startingPos + controlEffort;

    // Constrain the new servo position within limits
    newServoDir = constrain(newServoDir, 56, 122);

    // Update servo position
    myservo.write(newServoDir);
  }
}

void solenoidControl() {
  unsigned long currentTime = millis();

  if (solenoidState == HIGH && currentTime - previousTime >= interval_1) {
    previousTime = currentTime;
    solenoidState = LOW;
  }

  if (solenoidState == LOW && currentTime - previousTime >= interval_2) {
    previousTime = currentTime;
    solenoidState = HIGH;
  }

  digitalWrite(solenoidPin, solenoidState);
}

void finish() {
  if (millis() >= 75000) {
    delay(3600000);
  }
}
