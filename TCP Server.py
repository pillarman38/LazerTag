import time
import multiprocessing
import pygame
import socket
import threading
from queue import Queue


gameEnd = False
devastator = 0
valkirie = 0
trinity = 0
blitzfire = 0
wildfire = 0
gamma = 0

def calc_square(q):

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
    host = socket.gethostname()
    port = 5555
            
    serversocket.bind(("192.168.1.19", port))
            
    serversocket.listen(20)
            
    pygame.mixer.init()
    pygame.mixer.music.load("C:/Users/Owner/Desktop/Lazertag/Neal Acree Nightsong.mp3")
    pygame.mixer.music.play()

    time.sleep(10)
    
    while True:
        global gameEnd
        global valkirie
        global devastator
        global trinity
        global blitzfire
        global gamma

                        
        clientsocket,address = serversocket.accept()
                
        print("recieved connection from %s " % str(address))
                
        message = 'hello! Thankyou for connecting to the server' + "\r\n"
        
                
        clientsocket.send(message.encode('ascii'))
                
        messageTwo = clientsocket.recv(1024)
        messageThree = clientsocket.recv(1024)

                
        two = messageTwo.decode('ascii')
        three = messageThree.decode('ascii')
        
        print(two)
        print(three)
    
        if two == "This is Blitzfire":
            blitzfire += 10
            print(blitzfire)
        
        elif two  == "This is Valkirie":
            valkirie += 10
            print(valkirie)
            
        elif two == "This is Trinity":
            trinity += 10 
            print(trinity)
            
        elif two == "This is Gamma":
            gamma += 10
            print(gamma)
        if gameEnd == True:
            print('no')
            
            
            break
    print('connection closed')

def calc_cube(q):

    
    time.sleep(10)
    gameTimer = 0
    while gameTimer < 40:
        gameTimer += 1
        print(gameTimer)
        time.sleep(1)
        
        if gameTimer == 40:
            
            global gameEnd 
            gameEnd = True
            print([valkirie,devastator,blitzfire,wildfire,trinity,gamma])
            break
    

if __name__ == "__main__":
    q = Queue()
    
    p1 = threading.Thread(target=calc_square, args=(q, ))
    p2 = threading.Thread(target=calc_cube, args=(q, ))

    p1.start()
    p2.start()