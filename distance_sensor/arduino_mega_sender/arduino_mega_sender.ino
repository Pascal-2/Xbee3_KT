#include <Wire.h>

#define MEGA_SLAVE_ADDR 0x08

const int trigPin = 9;
const int echoPin = 10;

volatile int distanceCm = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Mega Sender Initialized");

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Wire.begin(MEGA_SLAVE_ADDR);

  Wire.onRequest(requestEvent); 
}

void loop() {
  long duration;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  int currentDistance = duration * 0.034 / 2;

  distanceCm = currentDistance;

  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.println(" cm");

  delay(100); 
}

void requestEvent() {
  byte highByte = highByte(distanceCm);
  byte lowByte = lowByte(distanceCm);
  
  Wire.write(highByte);
  Wire.write(lowByte);

  Serial.print("I2C Request. Sent: ");
  Serial.println(distanceCm);
}