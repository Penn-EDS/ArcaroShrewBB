import RPi.GPIO as GPIO
from time import sleep
# ---------------------------------------------------------------------------

#GPIO.setwarnings(False)  #Does not show warnings if the GPIO pins did not cleanup properly
GPIO.setmode(GPIO.BCM)  #Numbering according to BCM
    
pad1LED = 17
pad2LED = 18
pad3LED = 23

GPIO.setup(pad1LED, GPIO.OUT)  #Sets up GPIO as input or output
GPIO.setup(pad2LED, GPIO.OUT)
GPIO.setup(pad3LED, GPIO.OUT)

GPIO.output(pad1LED, False)
GPIO.output(pad2LED, False)
GPIO.output(pad3LED, False)

try:
    while True:
        GPIO.output(pad1LED, True)
        GPIO.output(pad2LED, True)
        GPIO.output(pad3LED, True)
        sleep(1)
        GPIO.output(pad1LED, False)
        GPIO.output(pad2LED, False)
        GPIO.output(pad3LED, False)
        sleep(1)
        
except (KeyboardInterrupt, SystemExit):  #Terminate program with CTRL + C
    print('Bye ;)')
    
    
finally:
    GPIO.cleanup()  #resets any ports you have used in this program back to input mode