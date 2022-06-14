#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 03/01/2022
# Revision ='1.0' 
#                 
# ---------------------------------------------------------------------------
"""
    Script that configures interrupts to detect the rising (pressing) and falling
    (release) edge of the capacitive touch sensors. Running this script or
    including it in another will have the Interrupt Service Routine for the
    selected GPIO active, no need to call functions.
"""
# ---------------------------------------------------------------------------

import RPi.GPIO as GPIO
import signal
import sys

# ---------------------------------------------------------------------------

from time import strftime, perf_counter_ns, sleep
from fileManage import *

# ---------------------------------------------------------------------------



GPIO.setmode(GPIO.BCM)

pad1 = 4  #GPIO ports for the touchpads
pad2 = 27
pad3 = 22

GPIO.setup(pad1, GPIO.IN) #Set GPIO pins as inputs
GPIO.setup(pad2, GPIO.IN)
GPIO.setup(pad3, GPIO.IN)

timeStart = perf_counter_ns()  
timeStamp = strftime("%Y-%m-%d_%H:%M:%S")  #String that contains the date in YYYY-MM-DD_HH:MM:SS format
fileName = 'Cap Touch Test'


dataList = ['Event Time,', 'Event,', 'Details', '\n']

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def pad1_pressed_callback(channel):  #Interrupt Service Routine for Pad1
    global timeStart  #Using the global variables not locals
    global timeStamp
    global fileName
    
    currentTime = perf_counter_ns() #To calculate current relative time
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad1):  #Event for when the pad is pressed
        storeEvent(timeStamp, fileName, [eventTime, ',', 'Pad1,', '1', '\n'])
        print('Pad1 pressed!')
    else:  #Event for when the pad is released
        storeEvent(timeStamp, fileName, [eventTime, ',', 'Pad1,', '0', '\n'])
        print('Pad1 released!')
        
def pad2_pressed_callback(channel):
    global timeStart
    global timeStamp
    global fileName
    
    currentTime = perf_counter_ns()
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad2):
        storeEvent(timeStamp, fileName, [eventTime,',', 'Pad2,', '1', '\n'])
        print('Pad2 pressed!')
    else:
        storeEvent(timeStamp, fileName, [eventTime,',', 'Pad2,', '0', '\n'])
        print('Pad2 released!')
        
def pad3_pressed_callback(channel):
    global timeStart
    global timeStamp
    global fileName
    
    currentTime = perf_counter_ns()
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad3):      
        storeEvent(timeStamp, fileName, [eventTime,',', 'Pad3,', '1', '\n'])
        print('Pad3 pressed!')
    else:
        storeEvent(timeStamp, fileName, [eventTime,',', 'Pad3,', '0', '\n'])
        print('Pad3 released!')
    
GPIO.add_event_detect(pad1, GPIO.BOTH, 
                        callback = pad1_pressed_callback)    
GPIO.add_event_detect(pad2, GPIO.BOTH, 
                        callback = pad2_pressed_callback)
GPIO.add_event_detect(pad3, GPIO.BOTH, 
                        callback = pad3_pressed_callback)
    
signal.signal(signal.SIGINT, signal_handler)
    
