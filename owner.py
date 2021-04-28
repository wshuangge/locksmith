
import paho.mqtt.client as mqtt
import time

led = 2
PORT = 3
button = 4

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    #client.subscribe("locksmith/detected")
    #client.message_callback_add("locksmith/detected",custom_callback_detected)

    client.subscribe("locksmith/password")
    client.message_callback_add("locksmith/password",custom_callback_password)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def custom_callback_detected(client, userdata, msg):
    print("custom_callback_detected: " + msg.topic + " " + str(msg.payload, "utf-8"))
    #display picture

def custom_callback_password(client, userdata, msg):
    print("custom_callback_password: " + msg.topic + " " + str(msg.payload, "utf-8"))
    pw=str(msg.payload, "utf-8")
    if pw==password:
        client.publish("locksmith/entry","True")
    else:
        client.publish("locksmith/entry","False")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    global password
    password=str(input("Enter Default Password (0-9): "));
    pw=-1
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        comm=input("Enter Password: ")
        password=comm
