# Concordia Capstone Project

The goal of our project is to design and build a system for filtering greenhouse effluent with a remote data management and collection system. This repository contains the software implementation of the client, server and embedded code that allows the user to collect and view data from our prototype.

## Client

## Server
Testing: run `coverage run manage.py test -v 2` from the `server` folder 

## Arduino

### Setup Instructions
Code is written for the nodeMCU v3 board. See instructions [here](https://www.instructables.com/Getting-Started-With-ESP8266LiLon-NodeMCU-V3Flashi/) for configuring your Arduino IDE, and a mapping of the nodeMCU's pins.

It is recommended to copy the arduino/arduino.cpp file and paste it into the Arduino IDE editor. 

At the top of the code you will see the following lines:

`const char* ssid = "****";`

`const char* password = "****";`

Be sure to replace the `****` with your WiFi network name and password before proceeding.