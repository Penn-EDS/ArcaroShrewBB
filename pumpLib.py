#!/usr/bin/env python3  
#----------------------------------------------------------------------------
# Created By  : Pedro V Quijano Carde 
# Created Date: 06/01/2022
# Revision ='1.0' 
#
# ---------------------------------------------------------------------------
""" This is the library file for the Highdriver4. It contains the following
    functions:

    -Highdriver4_init()
        This initializes all the highdriver4's registers
        and turns on the device (Powermode register set)
        
    -Highdriver4_setvoltage(pump, voltage)
        Sets the voltage for the selected channel, with pump being the
        channel number (1 through 4) and voltage (0 throught 250 V)
        
    -Highdriver4_setfrequency(frequency)
        Sets the frequency for all channels (50 through 800 Hz)
        
    -readRegisters()
        Prints the register values, most of them in binary. For debugging
"""
# ---------------------------------------------------------------------------

from smbus import SMBus

# ---------------------------------------------------------------------------

bPumpState = [False, False, False, False]    #Useful if need to have only one pump running at a time, and want the others off when calling a new pump to turn on. Would have to add a bit of code to the set voltage function. This was part of the C code from Bartels
nPumpVoltageByte = [0x00, 0x00, 0x00, 0x00]  #0x1F is maximum voltage (31, 5bits)
nFrequencyByte = 0x40 #Preset to 100Hz

# Define registers values from datasheet
    
I2C_DEVICEID = 0x00
I2C_POWERMODE = 0x01
I2C_FREQUENCY = 0x02
I2C_SHAPE = 0x03
I2C_BOOST = 0x04
I2C_PVOLTAGE = 0x06  #It appears to be on purpose
I2C_P1VOLTAGE = 0x06
I2C_P2VOLTAGE = 0x07
I2C_P3VOLTAGE = 0x08
I2C_P4VOLTAGE = 0x09
I2C_UPDATEVOLTAGE = 0x0A
I2C_AUDIO = 0x05

i2cbus = SMBus(1)  # Create a new I2C bus
I2C_HIGHDRIVER_ADRESS =0x7B #Default adress for mp-Highdriver4 11110XX
    
def Highdriver4_init(): #Initialize mp-Highdriver4
    global bPumpState 
    global nPumpVoltageByte
    
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_POWERMODE, 0x01) # Register 0x01 => 0x01 (enable)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_FREQUENCY, nFrequencyByte) # Register 0x02 => 0x40 (100Hz)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_SHAPE, 0x00) # Register 0x03 = 0x00 (sine wave)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_BOOST, 0x00) # Register 0x04 = 0x00 (800KHz)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_PVOLTAGE, 0x00) # Register 0x05 = 0x00 (audio off)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P1VOLTAGE, 0) # Register 0x06 = Amplitude1
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P2VOLTAGE, 0) # Register 0x07 = Amplitude2
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P3VOLTAGE, 0) # Register 0x08 = Amplitude3
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P4VOLTAGE, 0) # Register 0x09 = Amplitude4
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_UPDATEVOLTAGE, 0x01) # Register 0x0A = 0x01 (update)
    
    for i in range(4):   #Change contents of Pump State list to False
        bPumpState.pop(i)
        bPumpState.insert(i, False)
        
    for i in range(4):   #Change contents of Pump Voltage Byte list to 0x1F
        nPumpVoltageByte.pop(i)
        nPumpVoltageByte.insert(i, 0x1F)

def Highdriver4_setvoltage(pump, voltage): # Sets the voltage for the selected pump
    global bPumpState 
    global nPumpVoltageByte 
    global nFrequencyByte
    
    #print('Setting pump ', pump, ' at voltage ', voltage)  #For debugging
    temp = float(voltage)
    temp *= 31.0   #Voltage levels are asiggned with 5bits, so the decimal value is converted to 5bit
    temp /= 250.0  #Divides by 250 which is the maximum voltage for highdriver4
    
    if (pump>=1 and pump<=4):  #Makes sure that a valid pump was selected
        #nPumpVoltageByte[pump - 1] = constrain(temp,0,31) #Following if elif statement does this C/Arduino line of code
        if (temp > 31):    #Limits the max binary value to 31 (5bits available for voltage level
            tempConstrain = 31
        elif (temp < 0):   #Can not be a negative number
            tempConstain = 0
        else:
            tempConstrain = temp
            
        nPumpVoltageByte.pop(pump - 1)  #Change contents of PumpVoltageByte list 
        nPumpVoltageByte.insert(pump - 1, tempConstrain)
        
        bPumpState.pop(pump - 1)  #Change contents of selected pump in PumpState list  to True
        bPumpState.insert(pump - 1, True)
        
    #print('Voltage stored on list: ', nPumpVoltageByte[pump - 1])  #Debug
    #print('Pump Voltage List: ', nPumpVoltageByte)   #Debug

    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P1VOLTAGE, (int(nPumpVoltageByte[0]) if bPumpState[0] else 0))  # Writes to the register what is on PumpVoltageByte unless the corresponding PumpState is False (writes 0)
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P2VOLTAGE, (int(nPumpVoltageByte[1]) if bPumpState[1] else 0))
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P3VOLTAGE, (int(nPumpVoltageByte[2]) if bPumpState[2] else 0))
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P4VOLTAGE, (int(nPumpVoltageByte[3]) if bPumpState[3] else 0))
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_UPDATEVOLTAGE, 0x01)
   
   
def Highdriver4_setfrequency(frequency):  #Sets all channel frequency
    '''
    The frequency register uses the 6 least significant bits to
    choose the value inside of the range selected. The range is
    set with the 2 most significant bits, with 0b00 as 50 to 100,
    0b01 as 100-200 and so on.
    '''
    global nFrequencyByte
    
    if(frequency >= 800):  #800 Hz as maximum value
        nFrequencyByte = 0xFF
    elif (frequency >= 400):  # Range 400-800
        frequency -= 400  #Substracting the lower limit of the selected range
        frequency *= 64   #Conversion to 6bits
        frequency /= 400  #Divides to get a number from 0 to 1
        nFrequencyByte = int(frequency)|0xC0  #Sets the frequency two MSB to the appropriate value
    elif (frequency >= 200): # Range 200-400
        frequency -= 200
        frequency *= 64
        frequency /= 200
        nFrequencyByte = int(frequency)|0x80
    elif (frequency >= 100): # Range 100-200
        frequency -= 100
        frequency *= 64
        frequency /= 100
        nFrequencyByte = int(frequency)|0x40
    elif (frequency >= 50): # Range 50-100
        frequency -= 50
        frequency *= 64
        frequency /= 50
        nFrequencyByte = int(frequency)|0x00
    else: # outside of valid area
        nFrequencyByte = 0x00
        
    #print('Frequency set to: ', bin(nFrequencyByte))
        
    i2cbus.write_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_FREQUENCY, nFrequencyByte) # Writes register to input frequecy

def readRegisters():  #Reads and prints the highdriver4's registers
    addressRead = int()
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_DEVICEID)
    print('DeviceID: ', hex(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_POWERMODE) # Register 0x01 = 0x01 (enable)
    print('Powermode stored: ', bin(addressRead))

    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_FREQUENCY) # Register 0x02 = 0x40 (100Hz)
    print('Frequency stored: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_SHAPE) # Register 0x03 = 0x00 (sine wave)
    print('Shape stored: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_BOOST) # Register 0x04 = 0x00 (800KHz)
    print('Boost stored: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_AUDIO) # Register 0x05 = 0x00 (audio off)
    print('Audio stored: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P1VOLTAGE) # Register 0x06 = Amplitude1
    print('Channel 1 Voltage: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P2VOLTAGE) # Register 0x07 = Amplitude2
    print('Channel 2 Voltage: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P3VOLTAGE) # Register 0x08 = Amplitude3
    print('Channel 3 Voltage: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_P4VOLTAGE) # Register 0x09 = Amplitude4
    print('Channel 4 Voltage: ', bin(addressRead))
    
    addressRead = i2cbus.read_byte_data(I2C_HIGHDRIVER_ADRESS, I2C_UPDATEVOLTAGE) # Register 0x0A = 0x01 (update)
    print('Update Voltage: ', hex(addressRead))
