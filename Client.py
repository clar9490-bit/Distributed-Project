# create a socket for the client and connect to local host, then close the client

import socket


for i in range(100):
    client = socket.socket()

    client.connect(('127.0.0.1', 1005))

    print(client.recv(1024).decode())

    client.close()
