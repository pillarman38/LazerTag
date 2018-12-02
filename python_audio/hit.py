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
import threading

from gpiozero import PWMLED
# Ignore warning for now
gpio.setmode(gpio.BCM)
    # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #

gpio.setup(24, gpio.OUT, initial=gpio.LOW)
gpio.setup(8, gpio.OUT, initial=gpio.LOW)
  # Set GPIO pin 12 to output mode.
   # Initialize PWM on pwmPin 100Hz frequency
pi = pigpio.pi()

def processOne(q):
    global pi
    
    pi.set_PWM_dutycycle(18, 0)
    
    def repeatThis():
        ledFreq = 0   
##        while ledFreq < 255:
##            ledFreq += 1
##            pi.set_PWM_dutycycle(18, ledFreq)
##            time.sleep(0.01)
##            print(ledFreq)
##            if ledFreq == 255:
##                break
##        while ledFreq != 0:
##            ledFreq -= 1
##            pi.set_PWM_dutycycle(18, ledFreq)
##            time.sleep(0.01)
##            print(ledFreq)
    
        
        
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('poweringUpSound.mp3')
        pygame.mixer.music.play()
        
        while ledFreq < 255:
            ledFreq += 1
            pi.set_PWM_dutycycle(18, ledFreq)
            time.sleep(0.01)
            print(ledFreq)
            if ledFreq == 255:
                break
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
        
        while ledFreq != 0:
            ledFreq -= 1
            pi.set_PWM_dutycycle(18, ledFreq)
            time.sleep(0.001)
            print(ledFreq)
            if ledFreq == 0:
                break
        
        
        number = clientsocket.recv(1024)
        print(number)
            
        lirc.deinit()    
           
        time.sleep(10)
        
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('revive.mp3')
        pygame.mixer.music.play()
                
        print('rebooted')
        
    while True:
        repeatThis()

def processTwo(q, event):
    global pi

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
    
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('game-Over.mp3')
    pygame.mixer.music.play()
    ledFreq = 255
    while ledFreq != 0:
            ledFreq -= 1
            pi.set_PWM_dutycycle(18, ledFreq)
            time.sleep(0.01)
            print(ledFreq)
            if ledFreq == 0:
                break
    
def sender(q, event):
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
    event = multiprocessing.Event()
    
    p1 = multiprocessing.Process(target=processOne, args=(q,))
    p2 = multiprocessing.Process(target=processTwo, args=(q, event))
    p3 = threading.Thread(target=sender, args=(q, event))
    
    p1.start()
    p2.start()
    p3.start()
  
    p1.join()
    p2.join()
    p3.join()
        
        
        
    
    
        
    
