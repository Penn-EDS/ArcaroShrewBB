#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/13/2022
# Revision ='1.0' 
#                 
# ---------------------------------------------------------------------------
"""
    Script that uses polling every x seconds to determine the current state
    of the capacitive touch sensors. Uses the function from touch.py and
    prints the result.
    
    readTouch() - returns the state of all three sensors. Assing a variable
    to store the current state of each sensor. Returns boolean.
"""
# ---------------------------------------------------------------------------

from time import strftime, perf_counter, perf_counter_ns, sleep

# ---------------------------------------------------------------------------

from touch import *
from fileManage import *

# ---------------------------------------------------------------------------

header = ['Time\tWeight\n']  #Variables for file header
timeStart = perf_counter_ns() #CPU time to use as a time reference point
timeStamp = strftime("%Y-%m-%d_%H:%M:%S")  #String that contains the date in YYYY-MM-DD_HH:MM:SS format
fileName = 'Cap Poll Test' #Name for the data file

p1State = False #Variable to hold sensor state when read
p2State = False
p3State = False

storeEvent(timeStamp, fileName, header) #Create and store header on file

try:
    while True:
        p1State, p2State, p3State = readTouch() #Read the capacitive touch state
        print('Pad1 is ', p1State) #Print the sensor's state
        print('Pad2 is ', p2State)
        print('Pad3 is ', p3State)
        print('\n')
        sleep(1)
        
except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()