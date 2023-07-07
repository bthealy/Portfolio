#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <Servo.h>
#include "sensor_functions.h"
#include "control_functions.h"
#include "display_functions.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define Trig 10
#define Echo 2
#define Vx A0
#define Vy A1
#define Pin_elbow 4
#define Pin_gripper 5
#define Button 12
#define SlowSpeed 1
#define HighSpeed 3

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Servo elbowServo;
Servo gripperServo;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  sensorSetup();
  controlSetup();
  displaySetup();
}

void loop() {
  pulse();
  filter();
  speedSetting();
  controlElbow();
  controlGripper();
  updateDisplay();
}
