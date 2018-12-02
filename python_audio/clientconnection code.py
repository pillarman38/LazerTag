import socket

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 50000

clientsocket.connect(('192.168.1.19', port))

message = clientsocket.recv(1024)



print(message.decode('ascii'))