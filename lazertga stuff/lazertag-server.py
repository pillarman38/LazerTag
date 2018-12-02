import paho.mqtt.client as mqtt
import pygame
from time import sleep
import lazertaggui as gui
import gameVars as gv
import datetime 
import ast
import endGameGui

CLIENT = "192.168.1.19"
readyPlayers = 0
num_stats_received=0

def onConnect(client,userdata,flags,rc):
    if(rc==0):print("Connected")

def onSubscribe(client,userdata,mid,granted_qos):
    pass

def onMessage(client,userdata,message):
    global readyPlayers
    global num_stats_received
    if(message.payload.decode()=='ready'):
        readyPlayers+=1 
        print(readyPlayers,"player(s) in game lobby")
    else: #receive stats for end of game compilation
        num_stats_received+=1
        print(message.payload.decode())
        incoming_stats=ast.literal_eval(message.payload.decode())
        if(incoming_stats['player']=='1'):
            player1_stats=incoming_stats
        elif(incoming_stats['player']=='2'):
            player2_stats=incoming_stats
        elif(incoming_stats['player']=='3'):
            player3_stats=incoming_stats
def publishAll(message):
    print(message)
    server.publish('game/players',message)

def gameLobby():
    print("Waiting for other players...")
    
    selectedPlayerNum = gv.num_players

    while(readyPlayers<=selectedPlayerNum):
        
        if(readyPlayers==selectedPlayerNum):
            sleep(1)
            waitTime = gv.wait_time
            publishAll(str(gv_dict))
            sleep(0.1)
            publishAll("Starting game in "+str(waitTime)+" seconds...")
            
            while waitTime != 0:
                waitTime -= 1
                print(waitTime)
                sleep(1)
                if(waitTime == 0):
                    publishAll("start game")
                    
            break

server=mqtt.Client(client_id=CLIENT,clean_session=True)
server.on_connect=onConnect
server.on_subscribe=onSubscribe
server.on_message=onMessage

server.connect("192.168.1.19",keepalive=60,bind_address="")
server.loop_start()
server.subscribe('game/server',0)

while True:
    try:
        game_in_progress=True
        
        gv.init()

        gv_dict=dict(wait_time=gv.wait_time,num_players=gv.num_players,game_mode=gv.game_mode)
        
        print(gv_dict)
        server.publish('game/players',str(gv_dict))
        gameLobby()
        
        X = 1
        while game_in_progress == True:
            X -= 1
            result = str(datetime.timedelta(minutes = gv.timer, seconds= X))
            print(result)
            sleep(1)

            if(result == "0:00:00"):
                print("game Over")
                publishAll("Game Over")
                game_in_progress = False
                sleep(10)
                break
            
    except(KeyboardInterrupt):
        server.publish('game/players','exit')
        exit(0)
