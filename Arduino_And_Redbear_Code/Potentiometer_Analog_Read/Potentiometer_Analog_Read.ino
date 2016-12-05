/*
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
 * to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
 * and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 * 
 * Copyright (c) 2016 RedBear
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
 * IN THE SOFTWARE.
 */ 

/*
 * SYSTEM_MODE:
 *     - AUTOMATIC: Automatically try to connect to Wi-Fi and the Particle Cloud and handle the cloud messages.
 *     - SEMI_AUTOMATIC: Manually connect to Wi-Fi and the Particle Cloud, but automatically handle the cloud messages.
 *     - MANUAL: Manually connect to Wi-Fi and the Particle Cloud and handle the cloud messages.
 *     
 * SYSTEM_MODE(AUTOMATIC) does not need to be called, because it is the default state. 
 * However the user can invoke this method to make the mode explicit.
 * Learn more about system modes: https://docs.particle.io/reference/firmware/photon/#system-modes .
 */
#if defined(ARDUINO) 
SYSTEM_MODE(SEMI_AUTOMATIC); 
#endif

int colorPotValue;
int brightnessPotValue;
int kelvinPotValue;
int noisePotValue;
String msg; 

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  delay(5000);
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {

  noisePotValue = analogRead(A0);
//  Serial.print("Color");
//  Serial.println(colorPotValue);
//  delay(100);

  brightnessPotValue = analogRead(A1);
//  Serial.print("Brightness");
//  Serial.println(brightnessPotValue);
//  delay(100); 
  
  kelvinPotValue = analogRead(A2);
//  Serial.print("Kelvin");
//  Serial.println(kelvinPotValue);
//  delay(100);

  colorPotValue= analogRead(A3);
//  Serial.print("Noise");
//  Serial.println(noisePotValue);
//  delay(100);

  msg = "C" + (String)colorPotValue + "B" + (String)brightnessPotValue + "K" + (String)kelvinPotValue + "N" + (String)noisePotValue;
  Serial.println(msg);
  delay(500);
}


