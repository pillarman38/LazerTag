
import socket               # Import socket module
import threading
import pygame
import time
from queue import Queue

gamma = 0
blitzfire = 0
wildfire = 0
trinity = 0
valkirie = 0
devastator = 0

def processOne(q):

        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/Owner/Desktop/Lazertag/Neal Acree Nightsong.mp3")
        pygame.mixer.music.play()


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 50000                # Reserve a port for your service.

        print('Server started!')
        print ('Waiting for clients...')

        s.bind(("192.168.1.19", port))        # Bind to the port
        s.listen(5)                 # Now wait for client connection.
        time.sleep(10)
        def on_new_client(clientsocket,addr):
                global gamma
                global blitzfire
                global wildfire
                global trinity
                global valkirie
                global devastator
                while True:
                                
                        print("recieved connection from %s " % str(addr))
                                
                        message = 'hello! Thankyou for connecting to the server' + "\r\n"
                        game = "Game Over"
                                
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
                                
                        elif three == "This is Gamma":
                                gamma += 10
                                print(gamma)
                                
                        elif two == "Game Over":
                                print('no')

                       
        while True:
                c, addr = s.accept()     # Establish connection with client.
                print('Got connection from', addr)
                threading.Thread(target=on_new_client, args=(c,addr)).start()
                #Note it's (addr,) not (addr) because second parameter is a tuple
                #Edit: (c,addr)
                #that's how you pass arguments to functions when creating new threads using thread module.
def calc_cube(q):
    
    time.sleep(10)
    gameTimer = 0
    while gameTimer < 40:
        gameTimer += 1
        print(gameTimer)
        time.sleep(1)[]
        
        if gameTimer == 40:
            print([valkirie,devastator,blitzfire,wildfire,trinity,gamma])
            break

if __name__ == "__main__":
        q = Queue()

        threading.Thread(target=processOne, args=(q, )).start()
        threading.Thread(target=calc_cube, args=(q, )).start() 
