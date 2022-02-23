#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#include <Adafruit_AHTX0.h>

const char* ssid = "****";
const char* password = "****";

//enter the controller id and name here
const String controllerId = "1";
const String controllerName = "a";

float targetTemperature = 25.0;   //degrees celsius
float targetDepth = 0.50;         //meters

String baseUrl = "http://3.139.64.202/";  //TODO: update this every time the server is rebooted - need to assign domain name

//TODO: for testing, remove these later
String serverName = baseUrl + "/api/generic";
String queryString = "?sensor=temperature&start=1637105911&end=9999999999&controller=1";

unsigned long lastTime = 0;           //ms
unsigned long timerDelay = 5000;     //ms - set a 30 second delay between requests

Adafruit_AHTX0 aht; //for temp and humidity sensor

int pumpRelayPin = 15;

void setup() {
  Serial.begin(9600); 

  if (! aht.begin()) {
    Serial.println("Unable to find AHT sensor - check wiring");
    while (1) delay(10);
  }

  Serial.println("AHT sensor found");

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

  pinMode(pumpRelayPin, OUTPUT);
}

void loop() {
  // Send an HTTP POST request depending on timerDelay
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      // String result = getTemp(serverName, queryString);
      // String result = getTargets(baseUrl, controllerId);
      // sensors_event_t humidity, temp;
      // aht.getEvent(&humidity, &temp);

      float temperature = readTemperature();
      float humidity = readHumidity();

      Serial.print("Temperature: "); Serial.print(temperature); Serial.println(" degrees C");

      Serial.print("Humidity: "); Serial.print(humidity); Serial.println("% rH");

      // Serial.println(result);
    }
    else {
      Serial.println("WiFi Disconnected");
      //TODO: add function to blink LED to inform user of wifi disconnect
    }
    lastTime = millis();

    // String message = "Target temperature is: " + String(targetTemperature, 3);
    // Serial.println(message);
  }
}

String getTemp(String serverName, String queryString) {
  WiFiClient client;
  HTTPClient http;
  String serverPath = serverName + queryString;
  http.begin(client, serverPath.c_str());
  int httpResponseCode = http.GET();
  String payload = http.getString();
  http.end();
  if (httpResponseCode > 0) {
    return payload;
  } else {
    return "error";
  }
}

String postData(String serverName, String sensorType, String controllerName) {
  WiFiClient client;
  HTTPClient http;
  Serial.println("Beginning at url: " + serverName);
  http.begin(client, serverName.c_str());
  
  String postData = "sensor=" + sensorType + "&controller="+controllerName+"&value=55.01";
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

String getTargets(String baseUrl, String controllerId) {
  WiFiClient client;
  HTTPClient http;

  String requestUrl = baseUrl + "/api/target?id=" + controllerId;

  http.begin(client, requestUrl.c_str());

  int httpCode = http.GET();
  Serial.println(httpCode);
  String payload = http.getString();
  http.end();

  if (httpCode > 0) {
    Serial.println(httpCode);
    char json[100];
    payload.toCharArray(json, 100);
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, json);
    String status = doc["status"];
    Serial.println("Status is " + String(status));
    return payload;
  } else {
    return "error";
  }
}

// TODO: solve COM3 open port error
// TODO: solve separation of temp and humidity readings

float readTemperature() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  return temp.temperature;
}

float readHumidity() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  return humidity.relative_humidity;
}

void pumpOn() {
  digitalWrite(pumpRelayPin, HIGH);
}

void pumpOff() {
  digitalWrite(pumpRelayPin, LOW);
}