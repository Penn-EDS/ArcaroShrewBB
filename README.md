# ArcaroShrewBB
Dr. Arcaro's Shrew behavioral box software project in Python using the Raspberry PI as platform.  

The box incorporates a load cell to measure weight in grams, capacitive touch sensors that will sense the shrew's touch, and piezoelectric micropumps driven by the Highdriver4IC.

## Load Cell

The load cell used is an [Adafruit 4 wire Strain Gauge Load Cell](https://www.adafruit.com/product/4540) and the load cell amplifier used is the [Sparkfun's HX711 breakout board](https://www.sparkfun.com/products/13879). This board has the rate jumper that has been severed to have the sampling rate increased from 10 S/sec to 80 S/sec.

- The weightLib.py script handles the communication between the Raspberry Pi and the HX711. It has some modifications, but it is mostly the code from       [gandalf15](https://github.com/gandalf15/HX711). 

- The platformWeight.py script is a wrapper function for the weightLib function. It zeros the weight cell at the first call of the function, or when passing True as an argumen. There is a zero function in the HX711 library but did not seem to work at the time. Maybe in the future. Make sure there is nothing on the platform when first calling the function. Returns weight in grams and the most frequent maximum weight between 100 and 400 grams.
    
     - platformWeight() returns a weight in grams. If the swab file is not created
        the user is prompted to do so by calibrating the load cell.
    
        1. Before running the script make sure nothing is on the weight platform
        2. When asked put a known weight, wait for 3-5 seconds and press enter.
        3. When asked input the weight in grams and press enter
        4. The load cell is ready to use

## Capacitive Touch

The sensor used is the [AT42QT1010 breakout board from Adafruit](https://www.adafruit.com/product/1374), meaning the output will be Logic HIGH only when the sensor is being touched. Once released the output will go LOW. The connection to the copper plating included in the breakout board is severed with an X-Acto knife, ad well as a jumper for the included LED. a short cable is used to connect a small copper tape to the back side through hole that the copper pad used before.

- The touch.py script uses polling every x seconds (the user decides how quickly to poll) to determine the current state of the capacitive touch sensors.
    
     - readTouch() returns the state of all three sensors. Assing a variable to store the current state of each sensor. Returns boolean.

- The capTouch.py is script that configures interrupts to detect the rising (pressing) and falling (release) edge of the capacitive touch sensors. Running this script or including it in another will have the Interrupt Service Routine for the selected GPIO active, no need to call functions. Including this file as __from capTouch import \*__ will have the code on each callback function run each time the sensor is pressed and released, regardless of what is written on the main script.

- The capTouchandPollDemo.py is an example script that shows polling and interrupts for the capacitive touch sensors working at the same time.

## Pumps

The pumps used are the [mp6-liq piezoelectic pumps](https://www.servoflo.com/micropumps/mp6/mp6-micropump) made by Bartels and sold by Servoflo. They are driven by the [Highdriver4](https://www.servoflo.com/micropumps/mp6/kits-accessories).

- The pumpLib.py script is the library file for the Highdriver4. It contains the following
    functions:
    
     - Highdriver4_init() This initializes all the highdriver4's registers and turns on the device (Powermode register set)
        
     - Highdriver4_setvoltage(pump, voltage) Sets the voltage for the selected channel, with pump being the channel number (1 through 4) and voltage (0 throught 250 V)
        
     - Highdriver4_setfrequency(frequency) Sets the frequency for all channels (50 through 800 Hz)
        
     - readRegisters() Prints the register values, most of them in binary. For debugging

- The pumpTimeWrap.py script is a wrapper funtion to turn on the selected pump, and after the selected time has expired the same pump will be turned off.
    
     - timedPump(pump, voltage, timedispense)
         1. pump is to select the pump number (1 throught 4)
         2. voltage when turned on(0 through 250 V)
         3. timedispense (in seconds, can be fractional e.g. 0.5)

## Rotary Switch 
 
- The rotSwitch.py reads all the pins connected to the rotary switch and returns their state.

     - rotSwitchState() Read GPIO pin state, ordered from position 1 (leftmost) to position 6. Returns Boolean.

- The rotSwitchDemo.py is an example script showing the rotarySwitch working. Used for debugging purpuses.

## File Managing

Not hardware related. fileManage.py stores a text file.

   - storeEvent(timeStamp, fileName, data)

   - timestamp: includes the time in the file name, done outside with strftime("%Y-%m-%d_%H:%M:%S")
                    
   - filename: includes a string to the file name
        
   - data: this is what will be stored in the text file, can be integers, floating numbers, strings. For multiple inputs include them inside a list [var1, str1]. Format with \t and \n to import as delimited csv.
