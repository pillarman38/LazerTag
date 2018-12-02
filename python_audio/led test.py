import os, sys
from threading import Timer
import time
import RPi.GPIO as gpio

gpio.setwarnings(False) # Ignore warning for now
gpio.setmode(gpio.BCM)  # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #
gpio.setup(17, gpio.OUT, initial=gpio.LOW)
gpio.setup(24, gpio.OUT, initial=gpio.LOW)

for x in range(600): # Run forever
    gpio.output(24, gpio.HIGH) # Turn on
    time.sleep(0.3) # Sleep for 1 second
    gpio.output(24, gpio.LOW) # Turn off
           
    print("hi")
    gpio.output(24, gpio.HIGH) # Turn on
    time.sleep(0.3) # Sleep for 1 second
    gpio.output(24, gpio.LOW) # Turn off
    time.sleep(0.05)  
    
    
    gpio.output(24, gpio.HIGH) # Turn on
    time.sleep(0.3) # Sleep for 1 second
    gpio.output(24, gpio.LOW) # Turn off
     

    gpio.output(24, gpio.HIGH)# Turn on
    time.sleep(0.3) # Sleep for 1 second
    gpio.output(24, gpio.LOW)
