#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' 
#                 
# ---------------------------------------------------------------------------
""" Wrapper funtion to turn on the selected pump, and after the selected time
    has expired the same pump will be turned off.
    
    -timedPump(pump, voltage, timedispense)
        -Pump is to select the pump number (1 throught 4)
        -Voltage when turned on(0 through 250 V)
        -timedispense (in seconds, can be fractional e.g. 0.5)
"""
# ---------------------------------------------------------------------------

from threading import Timer

# ---------------------------------------------------------------------------

from pumpLib import *

# ---------------------------------------------------------------------------
    
def timedPump(pump, voltage, timedispense):
    t = Timer(timedispense, Highdriver4_setvoltage, [pump, 0])  #creates object t that defines the timer for the function to be called (Highdriver4_setvoltage) with arguments [pump, 0] when timedispense reaches 0. 
    Highdriver4_setvoltage(pump, voltage)
    t.start()
    
