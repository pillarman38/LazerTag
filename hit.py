import lirc
import os, sys
import socket, pickle
from threading import Timer
import time
import pygame
import RPi.GPIO as gpio
import multiprocessing
from multiprocessing import Queue

gpio.setwarnings(False) # Ignore warning for now
gpio.setmode(gpio.BCM)
    # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #
gpio.setup(18, gpio.OUT, initial=gpio.LOW)
gpio.setup(24, gpio.OUT, initial=gpio.LOW)
gpio.setup(8, gpio.OUT, initial=gpio.LOW)
p = gpio.PWM(18, 100)

def repeatThis():

    messageTwo = "valkirie hit"
                
    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    
    host = socket.gethostname

    port = 5555

    clientsocket.connect(('192.168.1.19', port))

    message = clientsocket.recv(1024)
        
    def dim():

            red_led = gpio.PWM(18,100)

            red_led.start(0)

            pause_time = 0.010

            for i in range(0,100+1):

                    red_led.ChangeDutyCycle(i)

                    time.sleep(pause_time)


                
                

    dim()
    p.start(100)	

    print(message.decode('ascii'))
                    
    sockid = lirc.init("myprogram") 
            
    lirc.nextcode()
        
    three = ''.join(lirc.nextcode()).replace("[|]", "")
        
    print(three)
               
    print('sent')
      
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('getHit.mp3')
    pygame.mixer.music.play()

    clientsocket.send(three.encode('ascii'))  
    clientsocket.send(messageTwo.encode('ascii'))
    number = clientsocket.recv(1024)
    print(number)
    
    clientsocket.close()
        
    lirc.deinit()
    p.stop(0)
    for x in range(6): # Run forever
        gpio.output(18, gpio.HIGH) # Turn on
        time.sleep(0.05) # Sleep for 1 second
        gpio.output(18, gpio.LOW) # Turn off
        time.sleep(0.05)            
        
    time.sleep(10)
            
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('revive.mp3')
    pygame.mixer.music.play()
            
    print('rebooted')
        
while True:
    repeatThis()
    

 