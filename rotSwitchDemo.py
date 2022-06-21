#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/20/2022
# Revision ='1.0'
#
# ---------------------------------------------------------------------------
""" This script is to test the rotary switch """
# ---------------------------------------------------------------------------

from time import sleep

# ---------------------------------------------------------------------------

from rotSwitch import *

# ---------------------------------------------------------------------------

try:
    
    pSW = False   #Flags for determining which position the rotary switch is in
    p1Clean = False
    p2Clean = False
    p3Clean = False
    standby = False
    testScript = False
    
    while True:
        standby, p1Clean, p2Clean, p3Clean, testScript, pSW = rotSwitchState()   #Read the GPIO pin's current state of the rotary switch
        
        print('\nPos1 is :', standby)
        print('Pos2 is :', p1Clean)
        print('Pos3 is :', p2Clean)
        print('Pos4 is :', p3Clean)
        print('Pos5 is :', testScript)
        print('Pos6 is :', pSW)
        
        sleep(1)
        
except (KeyboardInterrupt, SystemExit):  #Terminate program with CTRL + C
    print('Bye ;)')
    
    
finally:
    GPIO.cleanup()  #resets any ports you have used in this program back to input mode        