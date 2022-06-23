# ArcaroShrewBB
Dr. Arcaro's Shrew behavioral box software project in Python using the Raspberry PI as platform.  

The box incorporates a load cell to measure weight in grams, capacitive touch sensors that will sense the shrew's touch, and piezoelectric micropumps driven by the Highdriver4IC.

## Load Cell

The load cell used is an [Adafruit 4 wire Strain Gauge Load Cell](https://www.adafruit.com/product/4540) and the load cell amplifier used is the [Sparkfun's HX711 breakout board](https://www.sparkfun.com/products/13879)

The weightLib.py script handles the communication between the Raspberry Pi and the HX711. It has some modifications, but it is mostly the code from [gandalf15](https://github.com/gandalf15/HX711). 

The platformWeight.py script is a wrapper function for the weightLib function. It zeros the weight cell at the first call of the function, or when passing True as an argumen. There is a zero function in the HX711 library but did not seem to work at the time. Maybe in the future. Make sure there is nothing on the platform when first calling the function. Returns weight in grams and the most frequent maximum weight between 100 and 400 grams.
    
    -platformWeight() returns a weight in grams. If the swab file is not created
    the user is prompted to do so by calibrating the load cell.
    
    1. Before running the script make sure nothing is on the weight platform
    2. When asked put a known weight, wait for 3-5 seconds and press enter.
    3. When asked input the weight in grams and press enter
    4. The load cell is ready to use
