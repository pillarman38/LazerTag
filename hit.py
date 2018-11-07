import lirc
import os, sys
import socket, pickle
from threading import Timer
import time
import pygame
import multiprocessing
from multiprocessing import Queue
import RPi.GPIO as gpio
import pigpio
# Ignore warning for now
gpio.setmode(gpio.BCM)
    # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #
gpio.setup(18, gpio.OUT, initial=gpio.LOW)
gpio.setup(24, gpio.OUT, initial=gpio.LOW)
gpio.setup(8, gpio.OUT, initial=gpio.LOW)

gpio.setup(18, gpio.OUT)  # Set GPIO pin 12 to output mode.
pwm = gpio.PWM(18, 100)   # Initialize PWM on pwmPin 100Hz frequency

def processOne(q):
    global pwm
    global gpio
   
    def repeatThis():
        dc=0                               # set dc variable to 0 for 0%
        pwm.start(dc) 
        
        try:
                               # Loop until Ctl C is pressed to stop.
            for dc in range(100, -5, -5):    # Loop 0 to 100 stepping dc by 5 each loop
              pwm.ChangeDutyCycle(dc)
              time.sleep(0.05)
              # wait .05 seconds at current LED brightness
              
            
        except KeyboardInterrupt:
          print("Ctrl c to exit program")
        
        messageTwo = "valkirie hit"
                    
        clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        
        host = socket.gethostname

        port = 50000

        clientsocket.connect(('192.168.1.19', port))
        message = clientsocket.recv(1024)
        clientsocket.send(messageTwo.encode('ascii'))
        
        print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
        pwm.start(0)
        try:
                               # Loop until Ctl C is pressed to stop.
            for dc in range(0, 100, 5):    # Loop 0 to 100 stepping dc by 5 each loop
              pwm.ChangeDutyCycle(dc)
              time.sleep(0.05)             # wait .05 seconds at current LED brightness
              
            
        except KeyboardInterrupt:
            print("Ctr C to close program")
        
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
        
        
            
        lirc.deinit()
                                 # stop PWM
        try:
            for dc in range(100, -5, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
              pwm.ChangeDutyCycle(dc)
              time.sleep(0.05)             # wait .05 seconds at current LED brightness
              print(dc)
              
        except KeyboardInterrupt:
          print("Ctr C to close program")

                   
           
        time.sleep(10)
                
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('revive.mp3')
        pygame.mixer.music.play()
                
        print('rebooted')
        
    while True:
        repeatThis()

def processTwo(q):

    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        
    host = socket.gethostname

    port = 50001

    clientsocket.connect(('192.168.1.19', port))
    
  
    while True:
        message = clientsocket.recv(1024)
        decoded = message.decode('ascii')
        print(decoded)
        time.sleep(1)

        if decoded == "40":
            print("Game has ended")
            
            break
    
   
    try:
        for dc in range(100, -5, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
          pwm.ChangeDutyCycle(dc)
          time.sleep(0.05)             # wait .05 seconds at current LED brightness
          print(dc)
    except KeyboardInterrupt:
      print("Ctl C pressed - ending program")
    
    gpio.cleanup()
    pwm.stop
    
    
def sender(q):
    gpio.setmode(gpio.BCM)
    gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_UP)

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

if __name__ == "__main__":
    q = Queue()
    
    p1 = multiprocessing.Process(target=processOne, args=(q, ))
    p2 = multiprocessing.Process(target=processTwo, args=(q, ))
    p3 = multiprocessing.Process(target=sender, args=(q, ))
    
    p1.start()
    p2.start()
    p3.start()
    