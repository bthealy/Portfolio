#include <Arduino.h>
#include <Adafruit_SSD1306.h>
#include "display_functions.h"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void displaySetup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(WHITE);
  display.setTextSize(1);
}

void updateDisplay() {
  display.clearDisplay();

  const char* labels[] = {"Distance", "xValue", "yValue", "Elbow angle", "Gripper angle", "Speed"};
  int values[] = {filteredDistance, xValue, yValue, elbowAngle, gripperAngle, digitalRead(Button)};

  for (int i = 0; i < 6; i++) {
    display.setCursor(10, i * 10);
    display.print(labels[i]);
    display.print(" = ");
    display.print(values[i]);
  }

  display.setCursor(10, 50);
  display.print("Speed = ");
  display.print(values[5] ? "Slow" : "High");

  display.display();
}
