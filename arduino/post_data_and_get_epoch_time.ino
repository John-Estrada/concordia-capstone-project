#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

unsigned long epochTime; 

const char* ssid = "****";
const char* password = "****";

//enter the controller id and name here
const String controllerId = "1";
const String controllerName = "a";

String baseUrl = "http://johnestrada.org/api/";

unsigned long lastTime = 0;           //ms
unsigned long timerDelay = 5000;     //ms - set a 30 second delay between requests

void setup() {
  Serial.begin(9600); 
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("5 second delay before loop starts");

  epochTime = getTime();

  Serial.print("Epoch Time: ");
  Serial.println(epochTime);

}

void loop() {
  // Send an HTTP POST request depending on timerDelay
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){

      //example data string - use the format 'temperature,humidity,ec,ph'
      postData(baseUrl, "20.0,21.0,22.0,23.0");
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

String postData(String serverName, String data) {
  String requestURL = serverName + "datastring";
  WiFiClient client;
  HTTPClient http;
  Serial.println("Beginning at url: " + requestURL);
  http.begin(client, requestURL.c_str());

  Serial.println(epochTime + millis());
  
  String postData = "datastring=" + controllerName + "," + String(epochTime + millis()/1000)+"," + data;
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  
  int httpCode = http.POST(postData);
  Serial.println("Http code is: ");
  Serial.println(httpCode);
  
  if (httpCode > 0) {
    String payload = http.getString();
    return payload;
  } else {
    return "error " + httpCode;
  }
}

// Function that gets current epoch time
unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}