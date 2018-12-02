import os, sys
import socket

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                
host = socket.gethostname

port = 5555

clientsocket.connect(('192.168.1.19', port))
        
messageThree = "This is Trinity"
    
clientsocket.send(messageThree.encode('ascii'))  
        
clientsocket.close()

