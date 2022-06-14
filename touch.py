#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 02/12/2022
# Revision ='1.0' 
#                 
# ---------------------------------------------------------------------------
"""
    Script that uses polling every x seconds to determine the current state
    of the capacitive touch sensors.
    
    readTouch() - returns the state of all three sensors. Assing a variable
    to store the current state of each sensor. Returns boolean.
"""
# ---------------------------------------------------------------------------

import RPi.GPIO as GPIO

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------


GPIO.setmode(GPIO.BCM)

pad1 = 4  #GPIO ports for the touchpads
pad2 = 27
pad3 = 22

GPIO.setup(pad1, GPIO.IN) #Set GPIO pins as inputs
GPIO.setup(pad2, GPIO.IN)
GPIO.setup(pad3, GPIO.IN)

tIn1 = False #Variables to hold current sensor state
tIn2 = False
tIn3 = False

def readTouch(): #Function to read current sensor state
    tIn1 = GPIO.input(pad1)
    tIn2 = GPIO.input(pad2)
    tIn3 = GPIO.input(pad3)
    
    return tIn1, tIn2, tIn3 #Return the three pad's state in ascending order
        
        