
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
#import thread
import RPi.GPIO as GPIO
import time

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        return (characters[0])
    elif(GPIO.input(C2) == 1):
        return (characters[1])
    elif(GPIO.input(C3) == 1):
        return (characters[2])
    elif(GPIO.input(C4) == 1):
        return (characters[3])
    else:
        return ""
    GPIO.output(line, GPIO.LOW)

def read_password():
    stri=str(readLine(L1, ["1","2","3","A"]))+str(readLine(L2, ["4","5","6","B"]))+str(readLine(L3, ["7","8","9","C"]))+str(readLine(L4, ["*","0","#","D"]))
    time.sleep(2)
    return stri
    


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("locksmith/entry")
    client.message_callback_add("larrywan/entry",custom_callback_entry)

    client.subscribe("locksmith/detected")
    client.message_callback_add("locksmith/detected",custom_callback_detected)


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def custom_callback_entry(client, userdata, msg):
    print("custom_callback_entry: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global entry
    if(str(msg.payload, "utf-8")=="True"):
        entry=True
    else:
        entrt=False

def custom_callback_detected(client, userdata, msg):
    print("custom_callback_detected: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global detected
    if(str(msg.payload, "utf-8")=="True"):
        detected=True
    else:
        detected=False


def grant_entry(huh):
    if huh:
        print("Welcome")
    else:
        print("Leave Before I Call the Police!")
    time.sleep(3)



if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    detected=True
    while True:
        if(detected):
            password=""
            while(True):
                print(password)
                password+=read_password()
        time.sleep(0.3)

            

