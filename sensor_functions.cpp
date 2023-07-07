#include <Arduino.h>
#include "sensor_functions.h"

long duration;
int distance;
float filterValue = 0.4;
float filteredDistance = 0;
float previousFilteredDistance = 0;

void sensorSetup() {
  pinMode(Trig, OUTPUT);
  digitalWrite(Trig, LOW);
}

void pulse() {
  digitalWrite(Trig, LOW);
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig, LOW);
  duration = pulseIn(Echo, HIGH);
  distance = duration * 0.034 / 2;
}

void filter() {
  filteredDistance = filterValue * distance + (1 - filterValue) * previousFilteredDistance;
  previousFilteredDistance = filteredDistance;
}
