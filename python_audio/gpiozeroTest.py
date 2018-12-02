import time
import pigpio

pi = pigpio.pi()

ledFreq = 0
while True:
    while ledFreq < 255:
        ledFreq += 1
        pi.set_PWM_dutycycle(24, ledFreq)
        time.sleep(0.01)
        print(ledFreq)
        if ledFreq == 255:
            break
    while ledFreq != 0:
        ledFreq -= 1
        pi.set_PWM_dutycycle(24, ledFreq)
        time.sleep(0.01)
        print(ledFreq)
        
    
