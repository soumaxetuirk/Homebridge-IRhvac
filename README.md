# Homebridge-IRhvac
Control AC or thermostat using IRhvac (IRremoteESP8266) from homebridge. (built based on Tasmota)

This script connect homebridge-mqtthing and similar homebridge plugins with IRRemoteESP8266 IRhvac.

Any ESP8266 IR blaster can control thermostat or AC with IRremoteESP8266's IRhvac protocol.Tasmota firmware also includes IRremoteESP8266 Library.

WORKING PRINCIPLE:
Homebridge-Mqttthing sends all thermostat variables to diferent topics.This pythons scripts intercepts the messages and create proper json script and sends it to blaster in json format.

Tested on IRblaster running on tasmota firmware.

This is currently on alpha stage. Sooner a dedicated homebridge plugin will be developed.
