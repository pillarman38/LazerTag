import socket

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = '192.168.1.19'

port = 5555

clientsocket.connect(('192.168.1.19', port))

message = clienctsocket.recv(1024)

clientsocket.close()

print(message.decode('ascii'))
