import socket
from tkinter import filedialog

HOST = '127.0.0.1'
PORT = 1001

if __name__ == '__main__':

    # define a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # set options, bind socket to ip:port and listen on that address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)  # take max 10 connections
    data = filedialog.askopenfile(initialdir="/")
    path = str(data.name)
    image = open(path, "rb")
    print(f'socket listening on {server_socket.getsockname()}')

    while True:
        client, info = server_socket.accept()
        print(f'Got a connection from {(info)}')
        if client != 0:
            for i in image:
                client.send(i)
