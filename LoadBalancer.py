
# LoadBalancer is to distribute the work of the clients into the servers


from os import close
import random
import socket
import select
from itertools import cycle
import sys

HOST = '127.0.0.1'
PORT = 1005

SERVER_POOL = [('127.0.0.1', 1001), ('127.0.0.1', 1002), ('127.0.0.1', 1003), ]
ITERATOR = cycle(SERVER_POOL)

socket_queue = []
lookup = {}


def start_balancer():
    while True:
        # put clients into read mode
        read_sockets, write_sockets, error_sockets = select.select(
            socket_queue, [], [])
        for sock in read_sockets:
            if sock == client_sock:  # new connection
                accept_client()  # accept client
                break
            else:
                try:
                    data = sock.recv(4096)
                    if data:
                        receive(sock, data)
                    else:
                        close_socket(sock)
                        break
                except:
                    close_socket(sock)
                    break


def accept_client():
    sockfd, client_address = client_sock.accept()  # accept client
    print(
        f'Connected new client: {client_address} to {client_sock.getsockname()}')

    # pick a server
    ip_server, port_server = pick_server()

    # make connection to the server
    print(f'server socket located at: {(ip_server, port_server)}')

    client_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server_sock.connect((ip_server, port_server))
    print(f'client {client_address} connected to server {sockfd.getsockname()}')

    socket_queue.append(sockfd)
    socket_queue.append(client_server_sock)

    lookup[sockfd] = client_server_sock
    lookup[client_server_sock] = sockfd


def pick_server():
    return round_robin(ITERATOR)


def round_robin(iterate):
    return next(iterate)


def receive(socket: socket.socket, data):
    print(f'{socket.getpeername()} sent {socket.getsockname()}: {[data]}')
    local_socket = lookup[socket]
    local_socket.send(data)
    print(
        f'{local_socket.getsocketname()} sending {[data]} to {local_socket.getpeername()}')


def close_socket(socket: socket.socket):
    server_socket = lookup[socket]
    socket_queue.remove(socket)
    socket_queue.remove(server_socket)

    print(f'client {socket.getpeername()} disconnected')

    socket.close()
    server_socket.close()
    del lookup[socket]
    del lookup[server_socket]


client_sock = None
if __name__ == '__main__':
    # make a socket for the incoming client
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sock.bind((HOST, PORT))
    print(
        f'listening on: {client_sock.getsockname()}')
    client_sock.listen(10)  # max connections

    # add client to queue to go to server
    socket_queue.append(client_sock)
    start_balancer()
