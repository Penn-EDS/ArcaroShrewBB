import signal
import sys
import RPi.GPIO as GPIO

from time import perf_counter_ns, sleep
from touchFileManage2 import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pad1 = 4  #GPIO ports for the touchpads
pad2 = 27
pad3 = 22
trialButton = 26

GPIO.setup(pad1, GPIO.IN)
GPIO.setup(pad2, GPIO.IN)
GPIO.setup(pad3, GPIO.IN)
GPIO.setup(trialButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

timeStart = int()
dataList = ['Event Time,', 'Event,', 'Details', '\n']

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def pad1_pressed_callback(channel):
    global timeStart
    
    currentTime = 0
    currentTime = perf_counter_ns()
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad1):
        dataList.extend([eventTime, ',', 'Pad1,', '1', '\n'])
    else:
        dataList.extend([eventTime, ',', 'Pad1,', '0', '\n'])
        
def pad2_pressed_callback(channel):
    global timeStart
    
    currentTime = 0
    currentTime = perf_counter_ns()
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad2):
        dataList.extend([eventTime,',', 'Pad2,', '1', '\n'])
    else:
        dataList.extend([eventTime,',', 'Pad2,', '0', '\n'])
        
def pad3_pressed_callback(channel):
    global timeStart
    
    currentTime = 0
    currentTime = perf_counter_ns()
    eventTime = str((currentTime - timeStart) // 1000)
    
    if GPIO.input(pad3):
        dataList.extend([eventTime,',', 'Pad3,', '1', '\n'])
    else:
        dataList.extend([eventTime,',', 'Pad3,', '0', '\n'])
        
def trial_button_callback(channel):
    global dataList
    
    storeEvent(dataList)
    dataList.clear()
    dataList = ['Event Time,', 'Event,', 'Details', '\n']
    
def main():
    global timeStart
    
    GPIO.add_event_detect(pad1, GPIO.BOTH, 
                          callback = pad1_pressed_callback)    
    GPIO.add_event_detect(pad2, GPIO.BOTH, 
                          callback = pad2_pressed_callback)
    GPIO.add_event_detect(pad3, GPIO.BOTH, 
                          callback = pad3_pressed_callback)
    
    GPIO.add_event_detect(trialButton, GPIO.FALLING, 
                          callback=trial_button_callback, bouncetime=150)
    
    signal.signal(signal.SIGINT, signal_handler)
   
    print('Start Experiment')
    timeStart = perf_counter_ns()
    
    while True:
        print((perf_counter_ns() - timeStart) // 1000000000, 'seconds')
        sleep(1)
        
    signal.pause()     #Program pauses indefinitely, code after this will not run
    
if __name__ == '__main__':
    main()
