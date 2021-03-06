
#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' 
# ---------------------------------------------------------------------------
""" This script reads all the pins connected to the rotary switch and returns
    their state"""
# ---------------------------------------------------------------------------

import RPi.GPIO as GPIO

# ---------------------------------------------------------------------------

#GPIO.setwarnings(False)  #Does not show warnings if the GPIO pins did not cleanup properly
GPIO.setmode(GPIO.BCM)  #Numbering according to BCM
    
GPIO.setup(5, GPIO.IN)  #Sets up GPIO as input or output
GPIO.setup(6, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(19, GPIO.IN)

st1 = False  #Variable to store the pins state
st2 = False
st3 = False
st4 = False
st5 = False
st6 = False

def rotSwitchState():
    st1 = GPIO.input(19)  #Read GPIO pin state, ordered from position 1 (leftmost) to position 6.
    st2 = GPIO.input(16)
    st3 = GPIO.input(13)
    st4 = GPIO.input(12)
    st5 = GPIO.input(6)
    st6 = GPIO.input(5)
    
    return st1, st2, st3, st4, st5, st6  #Return the GPIO pin state in order 