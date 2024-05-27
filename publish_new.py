import datetime
import time
import threading
import paho.mqtt.client as mqtt
import json
import random
from datetime import datetime, timedelta
import string

TOTAL_PRODUCT_TOPIC = "FABLAB/MACHANICAL MACHINES/KB30/Metric/TotalProduct"
TOTAL_DEFECTIVE_TOPIC = "FABLAB/MACHANICAL MACHINES/KB30/Metric/TotalDefective"
MATERIAL_CODE_TOPIC = "FABLAB/MACHANICAL MACHINES/KB30/Metric/MaterialCode"

# --------------------------KB30-----------------------------------
MACHINE_STATUS_TOPIC1 = "FABLAB/MACHANICAL_MACHINES/KB30/Metric/MachineStatus"
MACHINE_POWER_TOPIC1 = "FABLAB/MACHANICAL_MACHINES/KB30/Metric/Power"
MACHINE_SPEED_TOPIC1 = "FABLAB/MACHANICAL_MACHINES/KB30/Metric/Speed"
MACHINE_VIBRATION_TOPIC1 = "FABLAB/MACHANICAL_MACHINES/KB30/Metric/Vibration"
MACHINE_OEE_TOPIC1 = "FABLAB/MACHANICAL_MACHINES/KB30/Metric/OEE"


# --------------------------máy cắt laser TSH1390-----------------------------------

MACHINE_STATUS_TOPIC2 = "FABLAB/MACHANICAL_MACHINES/TSH1390/Metric/MachineStatus"
MACHINE_POWER_TOPIC2 = "FABLAB/MACHANICAL_MACHINES/TSH1390/Metric/Power"
MACHINE_SPEED_TOPIC2 = "FABLAB/MACHANICAL_MACHINES/TSH1390/Metric/Speed"
MACHINE_VIBRATION_TOPIC2 = "FABLAB/MACHANICAL_MACHINES/TSH1390/Metric/Vibration"
MACHINE_OEE_TOPIC2 = "FABLAB/MACHANICAL_MACHINES/TSH1390/Metric/OEE"

# --------------------------máy khoan cần FRD900S-----------------------------------

MACHINE_STATUS_TOPIC3 = "FABLAB/MACHANICAL_MACHINES/FRD900S/Metric/MachineStatus"
MACHINE_POWER_TOPIC3 = "FABLAB/MACHANICAL_MACHINES/FRD900S/Metric/Power"
MACHINE_SPEED_TOPIC3 = "FABLAB/MACHANICAL_MACHINES/FRD900S/Metric/Speed"
MACHINE_VIBRATION_TOPIC3 = "FABLAB/MACHANICAL_MACHINES/FRD900S/Metric/Vibration"
MACHINE_OEE_TOPIC3 = "FABLAB/MACHANICAL_MACHINES/FRD900S/Metric/OEE"

# --------------------------máy tiện đa năng ERL1330-----------------------------------

MACHINE_STATUS_TOPIC4 = "FABLAB/MACHANICAL_MACHINES/ERL1330/Metric/MachineStatus"
MACHINE_POWER_TOPIC4 = "FABLAB/MACHANICAL_MACHINES/ERL1330/Metric/Power"
MACHINE_SPEED_TOPIC4 = "FABLAB/MACHANICAL_MACHINES/ERL1330/Metric/Speed"
MACHINE_VIBRATION_TOPIC4 = "FABLAB/MACHANICAL_MACHINES/ERL1330/Metric/Vibration"
MACHINE_OEE_TOPIC4 = "FABLAB/MACHANICAL_MACHINES/ERL1330/Metric/OEE"

MACHINE_HUMIDITY_TOPIC = "FABLAB/Environment/Metric/Humidity"
MACHINE_TEMPERATURE_TOPIC = "FABLAB/Environment/Metric/Temperature"
MACHINE_GAS_TOPIC = "FABLAB/Environment/Metric/Gas"
MACHINE_NOISE_TOPIC =  "FABLAB/Environment/Metric/Noise"

broker_address = "40.82.154.13" 
port = 1883 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print("Failed to connect, return code %d" % rc)

  
def Recreate_Data():
    Data_power = random.randint(80, 150)
    Data_speed = random.randint(80, 150)
    Data_Vibration = random.randint(80, 150)
    Data_Humidity = random.randint(70, 90)
    Data_Tempurature = random.randint(25, 35)
    Data_Gas = random.randint(80, 110)
    Data_Noise = random.randint(80, 150)


    messageMachineStatus = {

            "name": "MachineStatus",
            "value": 1,
            "timestamp":  str(datetime.now())
        
        }


    messagePower = {

            "name": "Power",
            "value": Data_power,
            "timestamp":  str(datetime.now())
        
        }
    messageSpeed = {

            "name": "Speed",
            "value": Data_speed,
            "timestamp":  str(datetime.now())
        
        }
    messageVibration = {

            "name": "Vibration",
            "value": Data_Vibration,
            "timestamp":  str(datetime.now())
        
        }
    messageHumidity = {

            "name": "Humidity",
            "value": Data_Humidity,
            "timestamp":  str(datetime.now())
        
        }
    messageTempurature = {

            "name": "Temperature",
            "value": Data_Tempurature,
            "timestamp":  str(datetime.now())
        
        }
    messageGas = {

            "name": "Gas",
            "value": Data_Gas,
            "timestamp":  str(datetime.now())
        
        }
    messageNoise = {

            "name": "Noise",
            "value": Data_Noise,
            "timestamp":  str(datetime.now())
        
        }
    messageoee = {
            "shiftTime": random.randint(100, 150),
            "idleTime": random.randint(80, 99),
            "operationTime": random.randint(60, 79),
            "timestamp":  str(datetime.now())
        
        }
    json_messageStatus = json.dumps(messageMachineStatus)


    json_messagePower = json.dumps(messagePower)
    json_messageSpeed = json.dumps(messageSpeed)
    json_messageVibration = json.dumps(messageVibration)
    json_messageHumidity = json.dumps(messageHumidity)
    json_messageTempurature = json.dumps(messageTempurature)
    json_messageGas = json.dumps(messageGas)
    json_messageNoise = json.dumps(messageNoise)
    json_messageoee = json.dumps(messageoee)
    return json_messageStatus,json_messagePower,json_messageSpeed,json_messageVibration,json_messageHumidity,json_messageTempurature,json_messageGas,json_messageNoise,json_messageoee



def Publish_Data1():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, port)
    client.loop_start()
    while True:
        json_messageStatus,json_messagePower,json_messageSpeed,json_messageVibration,json_messageHumidity,json_messageTempurature,json_messageGas,json_messageNoise,json_messageoee= Recreate_Data()
        
        client.publish(MACHINE_STATUS_TOPIC1,json_messageStatus,1,1)

      #  client.publish(OPERATIOR_TOPIC1,json_messageStaffID,1,1)

        client.publish(MACHINE_POWER_TOPIC1,json_messagePower,1,1)
        client.publish(MACHINE_SPEED_TOPIC1,json_messageSpeed,1,1)
        client.publish(MACHINE_VIBRATION_TOPIC1,json_messageVibration,1,1)
        client.publish(MACHINE_OEE_TOPIC1,json_messageoee,1,1)


        client.publish(MACHINE_HUMIDITY_TOPIC,json_messageHumidity,1,1)
        client.publish(MACHINE_TEMPERATURE_TOPIC,json_messageTempurature,1,1)
        client.publish(MACHINE_GAS_TOPIC,json_messageGas,1,1)
        client.publish(MACHINE_NOISE_TOPIC,json_messageNoise,1,1)

        time.sleep(10)

def Publish_Data2():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, port)
    client.loop_start()
    while True:
        json_messageStatus,json_messagePower,json_messageSpeed,json_messageVibration,json_messageHumidity,json_messageTempurature,json_messageGas,json_messageNoise,json_messageoee = Recreate_Data()
        
        client.publish(MACHINE_STATUS_TOPIC2,json_messageStatus,1,1)
       # client.publish(OPERATIOR_TOPIC2,json_messageStaffID,1,1)

        client.publish(MACHINE_POWER_TOPIC2,json_messagePower,1,1)
        client.publish(MACHINE_SPEED_TOPIC2,json_messageSpeed,1,1)
        client.publish(MACHINE_VIBRATION_TOPIC2,json_messageVibration,1,1)
        client.publish(MACHINE_OEE_TOPIC2,json_messageoee,1,1)

        time.sleep(10)

def Publish_Data3():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, port)
    client.loop_start()
    while True:
        json_messageStatus,json_messagePower,json_messageSpeed,json_messageVibration,json_messageHumidity,json_messageTempurature,json_messageGas,json_messageNoise,json_messageoee = Recreate_Data()
        
        client.publish(MACHINE_STATUS_TOPIC3,json_messageStatus,1,1)

        #client.publish(OPERATIOR_TOPIC3,json_messageStaffID,1,1)
        
        client.publish(MACHINE_POWER_TOPIC3,json_messagePower,1,1)
        client.publish(MACHINE_SPEED_TOPIC3,json_messageSpeed,1,1)
        client.publish(MACHINE_VIBRATION_TOPIC3,json_messageVibration,1,1)
        client.publish(MACHINE_OEE_TOPIC3,json_messageoee,1,1)

        time.sleep(10)

def Publish_Data4():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, port)
    client.loop_start()
    while True:
        json_messageStatus,json_messagePower,json_messageSpeed,json_messageVibration,json_messageHumidity,json_messageTempurature,json_messageGas,json_messageNoise,json_messageoee = Recreate_Data()
        
        client.publish(MACHINE_STATUS_TOPIC4,json_messageStatus,1,1)

        #client.publish(OPERATIOR_TOPIC4,json_messageStaffID,1,1)

        client.publish(MACHINE_POWER_TOPIC4,json_messagePower,1,1)
        client.publish(MACHINE_SPEED_TOPIC4,json_messageSpeed,1,1)
        client.publish(MACHINE_VIBRATION_TOPIC4,json_messageVibration,1,1)
        client.publish(MACHINE_OEE_TOPIC4,json_messageoee,1,1)

        time.sleep(1)



if __name__ == '__main__':
    thread1 = threading.Thread(target=Publish_Data1)
    thread2 = threading.Thread(target=Publish_Data2)
    thread3 = threading.Thread(target=Publish_Data3)
    thread4 = threading.Thread(target=Publish_Data4)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()









