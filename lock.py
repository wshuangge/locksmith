
from grove_rgb_lcd import *
from grovepi import *
import paho.mqtt.client as mqtt
import time
import threading
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














keypadPressed = -1

secretCode = "123"
input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global input
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("Password Reset");
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C4) == 1):
        client.publish("locksmith/password",input)
        pressed = True
        time.sleep(1)

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW)

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
        print("Entry Granted")
    else:
        print("Leave Before I Call the police")
    time.sleep(5)

def custom_callback_detected(client, userdata, msg):
    #print("custom_callback_detected: " + msg.topic + " " + str(msg.payload, "utf-8"))
    global detected
    if(str(msg.payload, "utf-8")=="True"):
        detected=True
    else:
        detected=False

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    detected=False
    state=0
    state1=0
    while True:
        print("No Face Detected\n")
        time.sleep(2)
        count=0
        if(detected):
            print("Face Detected\n")
            while True:
                print("Password Input:"+input)
                count+=1
                if(count>100):
                    print("Operation Time Expired\n")
                    break
                if keypadPressed != -1:
                    setAllLines(GPIO.HIGH)
                    if GPIO.input(keypadPressed) == 0:
                        keypadPressed = -1
                    else:
                        time.sleep(0.1)
                else:
                    if not checkSpecialKeys():
                        readLine(L1, ["1","2","3","A"])
                        readLine(L2, ["4","5","6","B"])
                        readLine(L3, ["7","8","9","C"])
                        readLine(L4, ["*","0","#","D"])
                        time.sleep(0.1)
                    else:
                        time.sleep(0.1)
            

