#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <time.h>

#define ssid     "OPPO"
#define password  "123456789"
#define ntpServer  "pool.ntp.org"
#define gmtOffset_sec  19800 // Indian Standard Time (IST) is GMT+5:30
#define daylightOffset_sec  0

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); 
    Serial.print(".");
  }
  Serial.println(" Connected to ");         
  Serial.print(" hotspot: ");     
  Serial.println(WiFi.localIP());              
  Serial.print(" wifi: ");    
  Serial.println(WiFi.softAPIP());           
  Serial.print(" Signal Strength ");           
  Serial.print(WiFi.RSSI());              
  Serial.println(" dBm");              
  Serial.print("Router IP ");          
  Serial.println(WiFi.gatewayIP());                 
  Serial.print(" Device MAC ");              
  Serial.println(WiFi.macAddress());

  // Initialize time with NTP server
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  // Wait for time to be set
  while (time(nullptr) < 1000) {
    delay(1000);
    Serial.println("Waiting for time synchronization...");
  }
}

void loop() {
  delay(1000);
  time_t now = time(nullptr);
  struct tm timeinfo;
  localtime_r(&now, &timeinfo);
  char time_str[40];
  strftime(time_str, sizeof(time_str), "%H:%M:%S  %d/%B/%Y  %A", &timeinfo);
  Serial.println(time_str);
}
