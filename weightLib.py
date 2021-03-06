#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' 
# ---------------------------------------------------------------------------
""" This script is use the load cell amplifier HX711 and get a measurement
    reading from the load cell. Much of the code was written by gandalf15,
    fount here: https://github.com/gandalf15/HX711
    
    -weight() returns a weight in grams. If the swab file is not created
    the user is prompted to do so by calibrating the load cell.
    
    1. Before running the script make sure nothing is on the weight platform
    2. When asked put a known weight, wait for 3-5 seconds and press enter.
    3. When asked input the weight in grams and press enter
    4. The load cell is ready to use
"""
# ---------------------------------------------------------------------------

import os
import pickle
import RPi.GPIO as GPIO  # import GPIO

# ---------------------------------------------------------------------------

from hx711 import HX711  # import the class HX711

# ---------------------------------------------------------------------------

def weight():
    
    correctMeasure = False #Flag for taking measurements below an absolute error
    accurate = False #Flag to decide whether weight measurement is more accurate
    speed = True   #Or quicker
    
    
    measure1 = 0
    measure2 = 0
    absError = 0

    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    
    # Check if we have swap file. If yes that suggest that the program was not
    # terminated proprly (power failure). We load the latest state.
    swap_file_name = 'swap_file.swp'
    if os.path.isfile(swap_file_name):
        with open(swap_file_name, 'rb') as swap_file:
            hx = pickle.load(swap_file)
            # now we loaded the state before the Pi restarted.
    else:
        # measure tare and save the value as offset for current channel
        # and gain selected. That means channel A and gain 128
        err = hx.zero()
        
        # check if successful
        if err:
            raise ValueError('Tare is unsuccessful.')

        reading = hx.get_raw_data_mean()
        
        if reading:  # always check if you get correct value or only False
            # now the value is close to 0
            print('Data subtracted by offset but still not converted to units:',
                  reading)
        else:
            print('invalid data', reading)

        # In order to calculate the conversion ratio to some units, in my case I want grams,
        # you must have known weight.
        input('Put known weight on the scale and then press Enter')
        reading = hx.get_data_mean()
        
        if reading:
            print('Mean value from HX711 subtracted by offset:', reading)
            known_weight_grams = input(
                'Write how many grams it was and press Enter: ')
            
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
                
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            # set scale ratio for particular channel and gain which is
            # used to calculate the conversion to units. Required argument is only
            # scale ratio. Without arguments 'channel' and 'gain_A' it sets
            # the ratio for current channel and gain.
            ratio = reading / value  # calculate the ratio for channel A and gain 128
            hx.set_scale_ratio(ratio)  # set ratio for current channel
            
            print('Ratio is set.')
            
        else:
            raise ValueError(
                'Cannot calculate mean value. Try debug mode. Variable reading:',
                reading)

        # This is how you can save the ratio and offset in order to load it later.
        # If Raspberry Pi unexpectedly powers down, load the settings.
        print('Saving the HX711 state to swap file on persistant memory')
        with open(swap_file_name, 'wb') as swap_file:
            pickle.dump(hx, swap_file)
            swap_file.flush()
            os.fsync(swap_file.fileno())
            # you have to flush, fsynch and close the file all the time.
            # This will write the file to the drive. It is slow but safe.
        input('Remove calibration weight and press Enter')
    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    #print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    #input('Press Enter to begin reading')
    
        
    correctMeasure = 0
        
    #while(not correctMeasure): #while statement to get consistant measurent
    if speed:
        measure1 = hx.get_weight_mean(20)
        
        return measure1
    
    elif accurate:
        while not correctMeasure:
            measure1 = hx.get_weight_mean(10)
            measure2 = hx.get_weight_mean(10)
            absError = abs(measure1 - measure2)  #Checks if the two measurements are similar
            
            if (absError < 5): #If they are the correct measurement is taken
                #print(format(measure1, '.2f'), 'g') #Debug
                correctMeasure = 1
                
            else: #If not the measurements are taken again
                print("Weighing")
                correctMeasure = 0
                
        return measure1
            