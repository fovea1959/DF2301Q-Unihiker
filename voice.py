#  -*- coding: UTF-8 -*-

import logging
import paho.mqtt.client as mqtt
from pinpong.board import Board,Pin
from unihiker import GUI

import time
#Download the DFRobot_DF2301Q.py library file suitable for UNIHIKER from this link and place it in the same folder as this program.
#https://github.com/DFRobot/DFRobot_DF2301Q/tree/master/python/unihiker
from DFRobot_DF2301Q import *

gui = GUI()
gui.fill_rect(x=0, y=0, w=240, h=320, color='#000000')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

Board().begin()
led = Pin(Pin.P24, Pin.OUT)  # Pin initialization to level output
DF2301Q = DFRobot_DF2301Q_I2C()  # Initialize
DF2301Q.set_volume(5)  # Volume
DF2301Q.set_mute_mode(0)  # Set mute
DF2301Q.set_wake_time(20)  # Set wake time
print(DF2301Q.get_wake_time())
DF2301Q.play_by_CMDID(2)
print("----------------------")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("mqtt.localnet", 1883, 60)

mqttc.loop_start()

while True:
    cmdid = DF2301Q.get_CMDID()
    if (not cmdid==0):
        gui.fill_rect(x=0, y=0, w=240, h=320, color='#000000')
        gui.draw_text(x=120, y=160, origin='center', text=str(cmdid), color='#00ffff')
        print(cmdid)
        mqttc.publish("unihiker/speech_command", str(cmdid))
    else:
        time.sleep(0.05)

