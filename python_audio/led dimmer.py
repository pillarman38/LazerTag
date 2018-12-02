import RPi.GPIO as gpio

import time

gpio.setwarnings(False) # Ignore warning for now
gpio.setmode(gpio.BCM)
    # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #
gpio.setup(18, gpio.OUT, initial=gpio.LOW)
gpio.setup(24, gpio.OUT, initial=gpio.LOW)
p = gpio.PWM(18, 100)

def dim():

	red_led = gpio.PWM(24,100)

	red_led.start(0)

	pause_time = 0.010

	for i in range(0,100+1):

		red_led.ChangeDutyCycle(i)

		time.sleep(pause_time)


	
	

dim()
p.start(100)	