#include <Wire.h>

const int trigPin = 9;  
const int echoPin = 10; 
float duration, distance;

void setup() {
  // put your setup code here, to run once:
  pinMode(trigPin, OUTPUT);  
	pinMode(echoPin, INPUT);  
	Serial.begin(9600);

  Wire.begin(8); // I2C Slave Adresse 8
  Wire.onReceive(receiveEvent);

}

void receiveEvent() {
  Serial.print("wurde nach Messung gefragt");
  uint32_t distanceBits = ((uint32_t)&distance);  // Reinterpret float as 4-byte int
  byte first_byte = distanceBits >> 24;
  byte second_byte = (distanceBits >> 16) & 0xFF;
  byte thrid_byte = (distanceBits >> 8) & 0xFF;
  byte fourth_byte = distanceBits & 0xFF;
  Wire.write(first_byte);
  Wire.write(second_byte);
  Wire.write(third_byte);
  Wire.write(fourth_byte); 
  
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, LOW);  
	delayMicroseconds(2);  
	digitalWrite(trigPin, HIGH);  
	delayMicroseconds(10);  
	digitalWrite(trigPin, LOW);  

  duration = pulseIn(echoPin, HIGH); 
  distance = (duration*.0343)/2;

  Serial.print("Distance: ");  
	Serial.println(distance);  
	delay(500);

}
