
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <ESP8266HTTPClient.h>
#include <EEPROM.h>

const char* ssid = "POCO X3 Pro";
const char* password = "1234567890";
const char* mqttServer = "broker.hivemq.com";
const char* clientID = "EspClient";
const char* trainTopic = "train";
const char* trainNumTopic = "train-num";
const String defaultTrainVar = "18233/2";
String trainVar;
String httpResp;
WiFiClient espClient;
PubSubClient client(espClient);

void writeWord(const String& word) {
  EEPROM.begin(512);
  for (int i = 0; i < word.length(); i++) {
    EEPROM.write(i, word[i]);
  }
  EEPROM.write(word.length(), '\0');
  EEPROM.commit();
  EEPROM.end();
}

String readWord() {
  EEPROM.begin(512);
  String word = "";
  char character = EEPROM.read(0);
  int i = 0;
  while (character != '\0') {
    word += character;
    i++;
    character = EEPROM.read(i);
  }
  EEPROM.end();
  return word;
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect((clientID + String(millis())).c_str())) {
      Serial.println("MQTT connected");
      client.subscribe(trainNumTopic);
    } else {
      Serial.printf("MQTT connection failed, rc=%d. Retrying in 5 seconds...\n", client.state());
      delay(3000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String rec;
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    rec += (char)payload[i];
  }
  Serial.print(" topic=[");
  Serial.print(topic);
  Serial.print("]  message=[");
  Serial.print(rec);
  Serial.println("]");

  if (strcmp(topic, trainNumTopic) == 0) {
    writeWord(rec);
    trainVar = readWord();
  } else {
    Serial.println("Unsubscribed topic");
  }
}

void manualControl() {
  client.publish(trainTopic, httpResp.c_str());
  delay(2000);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("WiFi connecting.");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);
}

void loop() {
  trainVar = readWord();
  if (trainVar <"1") {
    trainVar = defaultTrainVar;
  }

  if (!client.connected()) {
    reconnect();
  } else {
    manualControl();
  }
  client.loop();

  if (WiFi.status() == WL_CONNECTED) {
    BearSSL::WiFiClientSecure client;
    client.setInsecure();

    HTTPClient https;
    Serial.print("[HTTPS] Connecting...\n");

    if (https.begin(client, "https://train-54ut.onrender.com/" + trainVar)) {
      Serial.print("[HTTPS] GET...\n");
      int httpCode = https.GET();

      if (httpCode > 0) {
        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);

        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          httpResp = https.getString();
          Serial.println(httpResp);
        }
      } else {
        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }

      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }
  }

  Serial.println();
}
