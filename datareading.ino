#include <Wire.h>
#include <ADXL345.h>
ADXL345 accel;
int EN = 8; // I2C mode pin
unsigned long START; //assign a long type var
void setup()
{
  Serial.begin(9600);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, HIGH); //I2C is enabled
  if (!accel.begin())
  {
    Serial.println("error");
  }
  START = millis(); //keeps track of time (millis timer is an unsigned long var)
}
void loop()
{
  Vector raw = accel.readRaw(); //raw data reading
  if (millis() - START < 30000) //Output data rate is set to 100Hz by default
  {
    /* Serial.print(raw.XAxis);
      Serial.print("|");
      Serial.print(raw.YAxis);
      Serial.print("|");*/
    Serial.println(raw.ZAxis); //approx. 10.41ms
    delay(17.59); // sample rate control
  }
}
