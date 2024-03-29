/* This code is for executing the interrupt in ESP8266.
 The main purpose is to solve the ISR not in RAM isssue. */
#include <Arduino.h>
void ICACHE_RAM_ATTR ISRoutine ();
//D0,D8 interrut not wrk

void ISRoutine () {
   Serial.println("INTRERUPPT");
   digitalWrite(LED_BUILTIN,0);
}

void setup () {
 Serial.begin(115200);
 pinMode(D1,INPUT_PULLUP);
 pinMode(D3,INPUT_PULLUP); 
 pinMode(D6,INPUT_PULLUP); 
 pinMode(LED_BUILTIN,OUTPUT);
 attachInterrupt(digitalPinToInterrupt(D1),ISRoutine,RISING);
 attachInterrupt(digitalPinToInterrupt(D3),ISRoutine,CHANGE); 
 attachInterrupt(digitalPinToInterrupt(D6),ISRoutine,FALLING);  
}

void loop () {
  digitalWrite(LED_BUILTIN,1);
  delay(1000);  
  Serial.println("normal_run"); 
  delay(1000); 
}
