import paho.mqtt.client as mqtt
import lirc
from time import sleep
import RPi.GPIO as gpio
import pygame
import ast
from subprocess import call
import pigpio

CLIENT = "Valkyrie"
RELOAD = 16


connected = False
TRIGGER = 4
LTSERVER = '192.168.1.19'
connected = False
newgame = 'waiting'

gpio.setmode(gpio.BCM)
gpio.setup(TRIGGER, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(RELOAD, gpio.IN, pull_up_down=gpio.PUD_UP)

gpio.setmode(gpio.BCM)
    # Use physical pin numbering
gpio.setup(22, gpio.OUT, initial=gpio.LOW) #

gpio.setup(8, gpio.OUT, initial=gpio.LOW)
pi = pigpio.pi()

pi.set_PWM_dutycycle(18, 0)

ledFreq = 0

def onConnect(client,userdata,flags,rc):
    if(rc==0): print("Connected")
    client.subscribe('game/players')
    print("Waiting for other players...")
    
def ledsOn():
    global ledFreq
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('poweringUpSound.mp3')
    pygame.mixer.music.play()
    while ledFreq < 255:
        ledFreq += 1
        pi.set_PWM_dutycycle(24, ledFreq)
        sleep(0.001)
        
        if ledFreq == 255:
            break
        
def ledsOff():
    global ledFreq
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('poweringUpSound.mp3')
    pygame.mixer.music.play()
    
    
    while ledFreq <= 255:
        ledFreq -= 1
        pi.set_PWM_dutycycle(24, ledFreq)
        sleep(0.001)
        
        if ledFreq == 255:
            break
    
def onMessage(client,userdata,message):
    global gv_dict
    global stats
    global game_in_progress
    if message.payload.decode() == "Starting game in 5 seconds...":
        print("Starting game in 5 seconds")
        
    elif message.payload.decode() == "start game":
        game_in_progress = True
        print(message.payload.decode())
        ledsOn()
        
    elif message.payload.decode() == "Game Over":
        game_in_progress = False
        print(message.payload.decode())
        print(str(stats))
        player.publish('game/server', str(stats))
        ledsOff()
        print("Game has Ended! Return to base.")
        
    else:
        gv_dict=ast.literal_eval(message.payload.decode())
        print(message.payload.decode())
        print(stats)
        
def shoot(pin):
    global stats
    
    if stats['ammo'] == 0:
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('error.mp3')
        pygame.mixer.music.play()
    else:
        stats['ammo']-=1
        print(stats)
        print('Button Pressed')
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('blaster effect.mp3')
        pygame.mixer.music.play()
        call(['irsend', 'SEND_ONCE', 'SAMSUNG', 'KEY_3'])
        stats['shots_fired'] +=1
        
def reload(pin):
    global stats
    global maxAmmo
    
    if stats['ammo'] == 0:
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('reload.mp3')
        pygame.mixer.music.play()
        print(stats)
        stats['ammo']= maxAmmo

def initialize(gameMode):
    global maxAmmo
    global stats
    if gameMode == "Classic":
        print("Hello")
        maxAmmo = 10
        stats['ammo']=maxAmmo

#----------------------------------------------------------
#                        MAIN
#----------------------------------------------------------
try:
    player=mqtt.Client(client_id=CLIENT,clean_session=True)
    player.on_connect=onConnect
    player.on_message=onMessage
    
    game_in_progress=False
#    repeat=0
    gpio.add_event_detect(TRIGGER,gpio.RISING,shoot,bouncetime=400)
    gpio.add_event_detect(RELOAD,gpio.RISING,reload,bouncetime=400)

    while not connected:
        try:
            player.connect(LTSERVER,keepalive=60,bind_address="")
            connected=True
        except ConnectionRefusedError:
            print('LTServer must be started first...')
            
            sleep(1)
    connected=False

    while True:
        
        stats=dict(player=CLIENT,shots_fired=0,kills=0,deaths=0,health=0,ammo=0,)
        player.loop_start()
        player.publish('game/server','ready')

        while game_in_progress == False:
            pass #wait for start game message
        print("hi")
        initialize(gv_dict['game_mode'])
        
        sleep(5) #wait for processes to end
#        repeat_time=4
        while newgame=='waiting':
            
            sleep(1)
#            if repeat_time>0: 
#                repeat_time-=1
#                if repeat>=3:
#                    repeat=0
#                    player.publish('game/ltserver','repeat')
#                    print("Starting next game")
#                    break
            if newgame=='next':
                newgame=='waiting'
                print("Starting next game")
                break
            elif newgame=='exit':
                print("Exiting...")
                raise Exception

finally:
    gpio.cleanup()
    player.disconnect()

   