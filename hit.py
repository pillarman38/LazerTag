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


def processOne(q):
    
    def repeatThis():

        messageTwo = "valkirie hit"
                    
        clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        
        host = socket.gethostname

        port = 50000

        clientsocket.connect(('192.168.1.19', port))
        message = clientsocket.recv(1024)
        clientsocket.send(messageTwo.encode('ascii'))
        
       
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

def processTwo(q):
    
    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        
    host = socket.gethostname

    port = 50000

    clientsocket.connect(('192.168.1.19', port))
    message = clientsocket.recv(1024)
    clientsocket.close()

    gameTimer = 0
  
        
    while True:
        gameTimer += 1
        print(gameTimer)
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