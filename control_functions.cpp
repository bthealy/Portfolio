#include <Arduino.h>
#include "control_functions.h"
#include <algorithm>
#include <Servo.h>

int speed = 1;
int xValue = 0;
int yValue = 0;
int elbowAngle = 90;
int gripperAngle = 90;

void controlSetup() {
  elbowServo.attach(Pin_elbow);
  gripperServo.attach(Pin_gripper);
  pinMode(Button, INPUT_PULLUP);
  pinMode(Vx, INPUT);
  pinMode(Vy, INPUT);
}


void speedSetting() {
  speed = (digitalRead(Button) == 1) ? SlowSpeed : HighSpeed;
}


void controlElbow() {
  yValue = analogRead(Vy);

  if (yValue < 300)
    elbowAngle += speed;
  else if (yValue > 500)
    elbowAngle -= speed;

  elbowAngle = std::clamp(elbowAngle, 0, 180);  // Clamp the elbowAngle value
  elbowServo.write(elbowAngle);
}


void controlGripper() {
  xValue = analogRead(Vx);

  if (xValue < 300)
    gripperAngle += speed;
  else if (xValue > 500)
    gripperAngle -= speed;

  gripperAngle = std::clamp(gripperAngle, 60, 180);  // Clamp the gripperAngle value
  gripperServo.write(gripperAngle);
}
