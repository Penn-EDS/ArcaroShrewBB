#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' Add all modules currently used and make a simple script to
#                 use the rotary switch, pumps, and load cell.
# ---------------------------------------------------------------------------
""" This script is to demo all the functions for the hardware used in the
shrew box. """
# ---------------------------------------------------------------------------

from time import strftime, perf_counter, sleep

# ---------------------------------------------------------------------------
 
from fileManage import *
from platformWeight import *
from pumpLib import *
from pumpTimeWrap import *
from rotSwitch import *
from weightLib import *


# ---------------------------------------------------------------------------

try:
        
    pSW = False   #Flags for determining which position the rotary switch is in
    p1Clean = False
    p2Clean = False
    p3Clean = False
    p1cf = False  #Flag for having the corresponding pump turned on only once (send the command)
    p2vf = False
    p3cf = False 
    nosel = False  #Flag for having the pumps turned off only once when no valid position is selected on rotary switch
    cleaningDone = True #Flag to re-initialize the pumps after cleaning, set to true for first 
    weightM = 0
    
    timeStamp = strftime("%Y-%m-%d_%H:%M:%S")  #String that contains the date in YYYY-MM-DD_HH:MM:SS format
    fileName = "test"
    
    storeEvent(timeStamp, fileName, ["Test string"])
    
    Highdriver4_init()  #Initialize highdriver4 and have Powermode register set 
    
    platformWeight()
    
    while True:  #main loop
        
        pSW, p1Clean, p2Clean, p3Clean = rotSwitchState()   #Read the GPIO pin's current state of the rotary switch
        
        if pSW:  #Pumps run with software
            
            if cleaningDone:   #Only run when rotary switch first  selected pSW
                cleaningDone = False  #Will not run this if statement if the rotary switch stays on this position
                p1cf = False   #Resetting other flags
                p2vf = False
                p3cf = False
                nosel = False
                Highdriver4_setfrequency(100)     #Frequency for dispensing liquids
                Highdriver4_init()
                readRegisters()
                print("Pumps working normally\n")
                
            platformWeight()
            #weightM = weight()  #Get current weight on platform
            #print(weightM)
            sleep(1)
            
        elif p1Clean or p2Clean or p3Clean:  #Checks for other pins for cleaning
            Highdriver4_setfrequency(200)    #Different frequency for cleaning or priming
            
            cleaningDone = True #Resetting other flags
            nosel = False
            
            if p1Clean:
                if not p1cf: #Only run when rotary switch first  selected this
                    p1cf = True #Resetting other flags
                    p2cf = False
                    p3cf = False
                    
                    Highdriver4_setvoltage(1, 240)
                    Highdriver4_setvoltage(2, 0)
                    Highdriver4_setvoltage(3, 0)
                    
                    print('Cleaning Pump 1!\n')
                    readRegisters()
            elif p2Clean: 
                if not p2cf: #Only run when rotary switch first  selected this
                    p1cf = False #Resetting other flags
                    p2cf = True
                    p3cf = False
                    
                    Highdriver4_setvoltage(1, 0)
                    Highdriver4_setvoltage(2, 240)
                    Highdriver4_setvoltage(3, 0)
                    
                    readRegisters()
                    print('Cleaning Pump 2!\n')
                    
            elif p3Clean:
                if not p3cf: #Only run when rotary switch first  selected this
                    p1cf = False #Resetting other flags
                    p2cf = False
                    p3cf = True
                    
                    Highdriver4_setvoltage(1, 0)
                    Highdriver4_setvoltage(2, 0)
                    Highdriver4_setvoltage(3, 240)
                    
                    readRegisters()
                    print('Cleaning Pump 3!\n')
            
        else:
            if not nosel: #Only run when rotary switch first  selected this
                Highdriver4_init()
                i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_POWERMODE, 0x00) #Turn off highdriver4
                
                cleaningDone = True #Resetting other flags
                p1cf = False
                p2vf = False
                p3cf = False
                nosel = True
                
                readRegisters()
                print("No pumps selected, highdriver off\n")
            

except (KeyboardInterrupt, SystemExit):  #Terminate program with CTRL + C
    print('Bye :)')
    
    Highdriver4_init()  #Set all registers to default
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_POWERMODE, 0x00) #Turn off highdriver4
    
finally:
    GPIO.cleanup()  #resets any ports you have used in this program back to input mode