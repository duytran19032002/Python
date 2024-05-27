"""This code is used to read data from PLC Siemens S7-1200 through OPC UA protocol."""

import time
import json
import threading
import datetime
import os
import sys
import paho.mqtt.client as mqtt
from opcua import Client, ua

# --------------------- User variable --------------------------------------
lock = threading.Lock() # Called in thread to block the rest of threads

var_list = ["ns=4;i=9", "ns=4;i=10", "ns=4;i=8", "ns=4;i=15", "ns=4;i=7", "ns=4;i=16", "ns=4;i=14", "ns=4;i=12", "ns=4;i=11", "ns=4;i=13"]
old_value = [n * -1 for n in range(len(var_list))]

shotCount_var = "ns=4;i=12"
injTime_var = "ns=4;i=7"
bit_reset = "ns=4;i=17"

# Time of injection
injectionTime = 0
injectionCycle = 0

count_err = 0
prev_sign = 0
# ---------------------------------------------------------------------------


# --------------------- Foramt Json Payload ---------------------------------
def generate_data_status(state, value):
    data = [{
            "name": "machineStatus",
            "value": value,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }]
    return json.dumps(data)


def generate_data(data_name, data_value):
    data = [{
            "name": str(data_name),
            "value": data_value,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }]
    return json.dumps(data)
# ---------------------------------------------------------------------------


# -------------------------- User Functions ---------------------------------

def convert_time_to_milliseconds(time_of_day=datetime.time(0, 0, 0, 0)):
    # This function is used to convert time to miliseconds
    time_as_timedelta = datetime.timedelta(hours=time_of_day.hour, minutes=time_of_day.minute, seconds=time_of_day.second)
    time_as_milliseconds = int(time_as_timedelta.total_seconds() * 1000)
    return time_as_milliseconds


def convert_miliseconds_to_timeOfDay(time_as_milliseconds):
    # This function is used to convert time to miliseconds to timeofDay
    milliseconds = time_as_milliseconds
    time_as_timedelta = datetime.timedelta(milliseconds=milliseconds)
    hours, remainder = divmod(time_as_timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_of_day = datetime.time(hour=hours, minute=minutes, second=seconds)
    return time_of_day


def reset_program_SIEMENS():
    global bit_reset
    try:
        with lock:
            var_node = uaclient.get_node(str(bit_reset))
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            threading.Event().wait(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
            print("Reset SIEMENS successfully")
    except Exception as e:
        print(e)


def restart_python_program():
    python = sys.executable
    os.execl(python,python, *sys.argv)
# ------------------------------------------------------------------------


# ------------------------- Setup OPCUA ----------------------------------
# Check if Raspberry Pi / Laptop connect to PLC S7-1200
plc_addr = "192.168.0.1"
timeout_connect = 0

while True:
    # Uncomment following statement when using Raspberry Pi 
    # res = os.system("ping -c 1 " + str(eth0) + " > /dev/null 2>&1")

    # Uncomment following statement when using Laptop
    res = os.system("ping -n 1 " + str(plc_addr) + " > nul")
    time.sleep(1)

    if res == 0:
        print("Connected to the ip")
        break
    else:   
        print("No opcua connection.")
        if timeout_connect == 10:
            timeout_connect = 0
        timeout_connect += 1
        print(timeout_connect)

# Connect to OPC UA
url = "opc.tcp://192.168.0.1:4840"
uaclient = Client(url)
uaclient.connect()
print("ua client connected")

# Functions to get data from OPC 
def ua_getnodedata(ua_nodeid):
    ua = uaclient.get_node(str(ua_nodeid))
    ua_value = ua.get_value()
    ua_name = ua.get_display_name().Text
    # ua_name = ua.nodeid.__dict__['Identifier']
    return (str(ua_name), ua_value)


def ua_reconnect(url):
    uaclient = Client(url)
    uaclient.connect()
    print("ua client connected")
# ----------------------------------------------------------------------------


# --------------------------- Setup MQTT -------------------------------------
# Define MQTT call-back function
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from MQTT broker, storing messages...")


mqttBroker="mqtt.eclipseprojects.io"
# mqttBroker = "20.214.136.1"  # cloud
mqttPort = 1883
mqttKeepAliveINTERVAL = 45

# Initiate Mqtt Client
client = mqtt.Client("demo_raspi_HAITHIEN")

# if machine is TESTediately turned off --> last_will sends "Status: Off" to topic
client.will_set("HAITHIEN/I1/Metric/machineStatus", str(generate_data_status("Off", 5)), 1, 1)

# if the broker requires username and password
client.username_pw_set(username="username", password="password")

# Register callback function
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect with MQTT Broker
print("connecting to broker ", mqttBroker)

# Check connection to MQTT Broker
try:
    client.connect(mqttBroker, mqttPort, mqttKeepAliveINTERVAL)
except:
    print("Can't connect MQTT Broker!")

client.loop_start()
time.sleep(0.5)

client.publish("HAITHIEN/I1/Metric/machineStatus", str(generate_data_status("Run", 1)), 1, 1)
client.publish("HAITHIEN/I1/Metric/OPC_UA_Conection_status", "Connected")
# ----------------------------------------------------------------------------

# ------------------------------- MultiTasks ---------------------------------
def task_get_PLC_data():
    global injectionTime, count_err
    while True:
        try:
            for ua_nodeid in var_list:
                get_cycleTime(shotCount_var, injTime_var)
                with lock:
                    data_name, data_value = ua_getnodedata(ua_nodeid)
                    count_err = 0

                    if old_value[var_list.index(ua_nodeid)] == data_value:
                        continue

                    # Đặt lại tên biến theo yêu cầu
                    if data_name == "tmTemp1_Current":
                        data_name = "Nozzle Temp"
                    elif data_name == "tmInjMaxPress":
                        data_name = "Injection Peak Pressure"
                    elif data_name == "tmInjSpeed1":
                        data_name = "Peak Injection Speed"
                    elif data_name == "tmTurnPosi":
                        data_name = "Switch Over Pos"
                    elif data_name == "tmCycleTime":
                        injectionTime = data_value
                        data_name = "injectionTime"
                    elif data_name == "tmShotCount":
                        data_name = "counterShot"

                    data = generate_data(data_name, data_value)
                    mqtt_topic = "HAITHIEN/I1/Metric/" + str(data_name)
                    client.publish(mqtt_topic, str(data), 1, 1)
                    print(data)

                    old_value[var_list.index(ua_nodeid)] = data_value
                threading.Event().wait(0.01)

        except Exception as e:
            count_err += 1
            if count_err == 5:
                restart_python_program()
            print(e)
            client.publish("HAITHIEN/I1/Metric/OPC_UA_Conection_status", "Faild/Reconnect")
            print("Getting data from OPCUA UA is failed!")
            threading.Event().wait(1)


def get_cycleTime(signal_id, injTime_id, name_cycleTime="injectionCycle"):
    global injectionTime, injectionCycle, prev_sign
    try:
        with lock:
            _, new_sign = ua_getnodedata(signal_id)

            if new_sign != prev_sign:
                if (prev_sign != new_sign):  # Lúc này lấy thời điểm thay đổi giá trị của biến counterShot để làm mốc tính chu kỳ ép
                    new_time = datetime.datetime.now().time()

                    _, injTime_value = ua_getnodedata(injTime_id)
                    injectionCycle = injTime_value

                    cycleTime_post = generate_data(name_cycleTime, injectionCycle)
                    mqtt_topic = "HAITHIEN/I1/Metric/" + str(name_cycleTime)
                    client.publish(mqtt_topic, str(cycleTime_post), 1, 1)

                    old_time = new_time
                prev_sign = new_sign
        threading.Event().wait(0.01)

    except Exception as e:
        print(e)
        print("Failed to get cycleTime!")
        threading.Event().wait(0.5)
# ----------------------------------------------------------------------------

# ----------------------------- Main code ------------------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=task_get_PLC_data)

    t1.start()
    t1.join()
