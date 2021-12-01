import random
import socket
import select
from time import gmtime, strftime
from random import randint

imgcounter = 1
basename = "image%s.png"

HOST = '127.0.0.1'
PORT = 1004

connected_clients_sockets = []

# define a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set options, bind socket to ip:port and listen on that address
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)  # take max 10 connections

# add client to the queue
connected_clients_sockets.append(server_socket)

while True:
    # put clients into the read
    read_sockets, write_sockets, error_sockets = select.select(
        connected_clients_sockets, [], [])

    for sock in read_sockets:
        if sock == server_socket:  # new connection
            sockfd, client_address = server_socket.accept()  # accept client
            # connected_clients_sockets.append(sockfd)
        else:
            try:
                data = sock.recv(4096)
                txt = data.decode("utf-8")
                print(txt)
                if data:
                    if data.startswith('SIZE'):
                        tmp = txt.split()
                        size = int(tmp[1])

                        print('got size')

                        sock.sendall("GOT SIZE")

                    elif data.startswith('BYE'):
                        sock.shutdown()

                    else:

                        myfile = open(basename % imgcounter, 'wb')
                        myfile.write(data)

                        data = sock.recv(40960000)
                        if not data:
                            myfile.close()
                            break
                        myfile.write(data)
                        myfile.close()

                        sock.sendall("GOT IMAGE")
                        sock.shutdown()
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
        imgcounter += 1
server_socket.close()
# import socket
# import os
# from _thread import *
# from PIL import Image
#
# ServerSocket = socket.socket()
# host = '127.0.0.1'
# port = 1233
# ThreadCount = 0
# try:
#     ServerSocket.bind((host, port))
# except socket.error as e:
#     print(str(e))
#
# print('Waitiing for a Connection..')
# ServerSocket.listen(5)
#
#
# def threaded_client(connection):
#     connection.send(str.encode('Welcome to the Servern'))
#     while True:
#         data = connection.recv(2048)
#         reply = 'Server Says: ' + data.decode('utf-8')
#         if not data:
#             break
#         connection.sendall(str.encode(reply))
#     connection.close()
#
# while True:
#     Client, address = ServerSocket.accept()
#     print('Connected to: ' + address[0] + ':' + str(address[1]))
#
#     start_new_thread(threaded_client, (Client, ))
#     ThreadCount += 1
#     print('Thread Number: ' + str(ThreadCount))
# ServerSocket.close()
