/*!
 * MindPlus
 * telloesp32
 *
 */
#include <Arduino.h>



// Main program start
void setup() {
  Serial.begin(115200);
  Serial.println("hello");
}
void loop() {
  Serial.println("REPEAT");
  Serial.println((analogRead(13)));
  Serial.println((analogRead(14)));
  delay(1000);
}
