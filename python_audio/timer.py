import subprocess
import time
import hit.py

gameTimer = 0

while True:
    gameTimer += 1
    time.sleep(1)

    if gameTimer == 40:
        print("Game has ended")
        break
def dimmer():

    red_led = gpio.PWM(18,100)

    red_led.start(100)
    
    pause_time = 0.010

    for i in range(100,0+1):

        red_led.ChangeDutyCycle(i)

        time.sleep(pause_time)

dimmer()