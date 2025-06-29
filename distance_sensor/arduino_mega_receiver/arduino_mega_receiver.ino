#include <Wire.h>

#define NANO_SLAVE_ADDR 0x09

const int ledPin = 9; 

volatile int distanceCm = 0;

void setup() {

  Serial.begin(9600);
  Serial.println("Nano Receiver Initialized");

  pinMode(ledPin, OUTPUT);

  Wire.begin(NANO_SLAVE_ADDR);

  Wire.onReceive(receiveEvent); 
}

void loop() {

  int minDistance = 5;
  int maxDistance = 100;

  int constrainedDist = constrain(distanceCm, minDistance, maxDistance);
  int brightness = map(constrainedDist, minDistance, maxDistance, 255, 0);

  analogWrite(ledPin, brightness);

  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.print(" cm -> Brightness: ");
  Serial.println(brightness);

  delay(50);
}

void receiveEvent(int howMany) {
  if (howMany == 2) {
    byte highByte = Wire.read();
    byte lowByte = Wire.read();

    distanceCm = (highByte << 8) | lowByte;

    Serial.print("I2C Received: ");
    Serial.println(distanceCm);
  }

  while (Wire.available() > 0) {
    Wire.read();
  }
}