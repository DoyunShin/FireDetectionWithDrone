#include <MPU6050.h>
#include <RMTT_Libs.h>
//#include <RMTT_Shell.h>
#include <Wire.h>
#include <stdio.h>
#include <string.h>
#include "io_ctrl.h"

#define CommonSerial Serial
#define SDK_VERSION "esp32v2.0.0.5"

int ext_cmd_callback(int argc, char *argv[], char argv2[]);
int led_callback(int argc, char *argv[], char argv2[]);
void led_task(void *pParam);


MPU6050 mpu;

void setup()
{
  Serial.begin(115200);

  //Wire.begin(13, 14);
  //Wire.setClock(400000);
  Serial.println();
  Serial.println("Initialize MPU6050");
  Serial.println(SDK_VERSION);
  Serial.println();

  io_init();
  //shell_cmd_init();

  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    //while (!mpu.begin(13, 14)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    Serial.println("\n\n\n");
    delay(500);
  }

  //xTaskCreateUniversal(user_task, "user_task", 8192, NULL, 1, &userTaskHandle, 0);
}

void loop()
{
  Serial.println("ONLOOP");

  Vector normAccel = mpu.readNormalizeAccel();

  // Calculate Pitch & Roll
  int pitch = -(atan2(normAccel.XAxis, sqrt(normAccel.YAxis * normAccel.YAxis + normAccel.ZAxis * normAccel.ZAxis)) * 180.0) / M_PI;
  int roll = (atan2(normAccel.YAxis, normAccel.ZAxis) * 180.0) / M_PI;

  // Output
  Serial.print(" Pitch = ");
  Serial.print(pitch);
  Serial.print(" Roll = ");
  Serial.print(roll);

  Serial.println();

  delay(10);
}
