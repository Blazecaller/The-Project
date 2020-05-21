#include <MPU6050_tockn.h>
#include <Wire.h>
MPU6050 mpu6050(Wire);
long timer = 0;
void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();
  mpu6050.setGyroOffsets(2.66, -3.84, -0.47); // calibrated gyroscope parameters 
  // timer = millis(); // set the timer.
}
void loop() {
  mpu6050.update();
  Serial.print(mpu6050.getAngleX());
  Serial.print(",");
  Serial.print(mpu6050.getAngleY());
  Serial.print(",");
  Serial.print(mpu6050.getAngleZ());
  Serial.print("\n");
}
