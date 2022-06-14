#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 05/25/2022
# Revision ='1.0' 
#                 
# ---------------------------------------------------------------------------
"""
    Script to test the HX711 load cell amplifier. 
"""
# ---------------------------------------------------------------------------

import os
import pickle
import RPi.GPIO as GPIO  # import GPIO
from time import strftime, perf_counter, perf_counter_ns, sleep

# ---------------------------------------------------------------------------

from fileManage import *
from hx711 import HX711  # import the class HX711

# ---------------------------------------------------------------------------


correctMeasure = False #Flag for taking measurements below an absolute error
measure1 = 0
measure2 = 0
absError = 0
num = 0  #X axis
header = ['Time\tWeight\n']
timeStamp = strftime("%Y-%m-%d_%H:%M:%S")  #String that contains the date in YYYY-MM-DD_HH:MM:SS format
fileName = 'weightTest'




try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=21, pd_sck_pin=20)
    # Check if we have swap file. If yes that suggest that the program was not
    # terminated properly (power failure). We load the latest state.
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

    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    #input('Press Enter to begin reading')
    storeEvent(timeStamp, fileName, header)
    while True:
        num = num + 1
        correctMeasure = 0
        while(not correctMeasure):
            measure1 = hx.get_weight_mean(20)
            measure2 = hx.get_weight_mean(20)
            absError = abs(measure1 - measure2)
            #if (absError < 0.25): #For testing
            if (absError < .5):
                print('Success', format(measure1, '.2f'), 'g')
                storeEvent(timeStamp, fileName, [str(num), '\t',format(measure1, '.2f'), '\n'])
                correctMeasure = 1
            else:
                #print("Measurements too disimilar, trying again...")
                print("Inv Reading")
                print('Measure1 is ', measure1, ' and measure2 is ', measure2)
                correctMeasure = 0
                
            
            

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()