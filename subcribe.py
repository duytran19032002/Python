import time
import paho.mqtt.client as mqtt
import json
import random

broker_address = "test.mosquitto.org"
port = 1883

def on_state_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe("your/topic")
    else:
        print("Failed to connect, return code %d" % rc)

def on_message(client, userdata, msg):
    print("Received topic: " + msg.topic)
    print("Received message: " + str(msg.payload))
    client.subscribe("your/topic")

def on_subcribe():
    client = mqtt.Client()
    client_connectient = on_state_connect
    client.on_message = on_message
    client.connect(broker_address, port)
    client.loop_forever()

on_subcribe()
