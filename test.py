#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 05/31/2022
# Revision ='1.0' 
# ---------------------------------------------------------------------------
""" This script is for the test script. """
# ---------------------------------------------------------------------------

from time import strftime, perf_counter, perf_counter_ns, sleep

# ---------------------------------------------------------------------------

from touch import *
from pumpLib import *
from pumpTimeWrap import *

# ---------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)  #Numbering according to BCM
    
pad1LED = 17
pad2LED = 18
pad3LED = 23

GPIO.setup(pad1LED, GPIO.OUT)  #Sets up GPIO as input or output
GPIO.setup(pad2LED, GPIO.OUT)
GPIO.setup(pad3LED, GPIO.OUT)

GPIO.output(pad1LED, False)
GPIO.output(pad2LED, False)
GPIO.output(pad3LED, False)

def testFunc():
    Highdriver4_setfrequency(50)
    
    p1State = False #Variable to hold sensor state when read
    p2State = False
    p3State = False
    
    p1State, p2State, p3State = readTouch() #Read the capacitive touch state
    print('Pad1 is ', p1State) #Print the sensor's state
    print('Pad2 is ', p2State)
    print('Pad3 is ', p3State)
    print('\n')
    
    if p1State:
        timedPump(1, 200, 0.4)
        GPIO.output(pad1LED, True)
    else:
        GPIO.output(pad1LED, False)
        
    if p2State:
        timedPump(2, 200, 0.4)
        GPIO.output(pad2LED, True)
    else:
        GPIO.output(pad2LED, False)
    if p3State:
        timedPump(3, 200, 0.4)
        GPIO.output(pad3LED, True)
    else:
        GPIO.output(pad3LED, False)
    
    
    