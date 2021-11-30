import random
import socket, select
from time import gmtime, strftime
from random import randint

 #image path
image = "Meguim.png"

HOST = '127.0.0.1'
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

try:

    # open image
    myfile = open(image, 'rb')
    bytes = myfile.read()
    size = len(bytes)

    # send image size to server
    sock.sendall(str.encode("SIZE %s" % size))
    answer = sock.recv(4096)

    print('answer = %s' % answer)

    # send image to server
    if answer == 'GOT SIZE':
        sock.sendall(bytes)

        # check what server send
        answer = sock.recv(4096)
        print('answer = %s' % answer)

        if answer == 'GOT IMAGE' :
            sock.sendall("BYE BYE ")
            print('Image successfully send to server')

    myfile.close()

finally:
    sock.close()
# import socket
#
# ClientSocket = socket.socket()
# host = '127.0.0.1'
# port = 1233
#
# print('Waiting for connection')
# try:
#     ClientSocket.connect((host, port))
# except socket.error as e:
#     print(str(e))
#
# Response = ClientSocket.recv(1024)
# while True:
#     Input = input('Say Something: ')
#     ClientSocket.send(str.encode(Input))
#     Response = ClientSocket.recv(1024)
#     print(Response.decode('utf-8'))
#
# ClientSocket.close()