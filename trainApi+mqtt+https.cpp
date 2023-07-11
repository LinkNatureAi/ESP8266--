//this code build LinkNatureAi(SONU KOL)
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "POCO X3 Pro";
const char* password = "1234567890";
const char* mqttServer = "broker.hivemq.com";
const char* clientID = "EspClient";
const char* SendTrain = "train";
const char* train_num = "train-num";

String train_var = "18233/2";
String http_resp;
WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {
  while (!client.connected()) {
    if (client.connect((clientID + String(millis())).c_str())) {
      Serial.println("MQTT connected");
      client.subscribe(train_num);
    } else {
      Serial.printf("failed, rc=%d, try again in 5 seconds\n", client.state());
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String rec = String((char*)payload).substring(0, length);
  Serial.printf("topic=[%s] message=[%s]\n", topic, rec.c_str());

  if (strstr(topic, train_num)) {
    train_var = String(rec);
  } else {
    Serial.println("unsubscribed topic");
  }
}

void man_control() {
  client.publish(SendTrain, String(http_resp).c_str());
  delay(3000);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("WiFi connecting.");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqttServer, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  } else {
    man_control();
  }
  client.loop();

   if (WiFi.status() == WL_CONNECTED) {
    std::unique_ptr<BearSSL::WiFiClientSecure> client(new BearSSL::WiFiClientSecure);
    client->setInsecure();
    
    HTTPClient https;
    Serial.print("[HTTPS] begin...\n");
    
    if (https.begin(*client, "https://train-54ut.onrender.com/"+String(train_var))) {
      Serial.print("[HTTPS] GET...\n");
      int httpCode = https.GET();
      
      if (httpCode > 0) {
        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);
        
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          http_resp = https.getString();
          Serial.println(http_resp);
        }
      } else {
        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }
      
      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }
  }
 Serial.println("\n");
}
