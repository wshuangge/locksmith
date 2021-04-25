
import paho.mqtt.client as mqtt
import time
import threading

led = 2
PORT = 3
button = 4

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("locksmith/detected")
    client.message_callback_add("locksmith/detected",custom_callback_detected)

    client.subscribe("locksmith/password")
    client.message_callback_add("locksmith/password",custom_callback_password)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def custom_callback_detected(client, userdata, msg):
    print("custom_callback_alter: " + msg.topic + " " + str(msg.payload, "utf-8"))
    #display picture

def custom_callback_password(client, userdata, msg):
    print("custom_callback_password: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global pw
    pw=str(msg.payload, "utf-8")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    password=input("Enter Default Password (0-9): ");
    while True:  
        if(pw==password):
            client.publish("locksmith/entry",True)
        else:
            client.publish("locksmith/entry",False)
        comm=input("Enter 0 to change password")
        if(comm==0):
            password=comm