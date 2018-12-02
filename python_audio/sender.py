import RPi.GPIO as gpio
import time
import os
import pygame

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

while True:
    input_state = gpio.input(4)
    if input_state == False:
        print('Button Pressed')
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('blaster effect.mp3')
        pygame.mixer.music.play()
        os.system('irsend SEND_ONCE SAMSUNG KEY_3')
        
        time.sleep(0.02)
