

import random
import socket
import select
from itertools import cycle
import sys

HOST = '127.0.0.1'
PORT = 1000

SERVER_POOL = [('127.0.0.1', 1001), ('127.0.0.1', 1002), ('127.0.0.1', 1003), ]
ITERATOR = cycle(SERVER_POOL)


class LoadBalancer():
    client_socket_queue = []

    def __init__(self, port, ip='127.0.0.1') -> None:
        self.ip = ip
        self.port = port

        # make a socket for the incoming client
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_sock.bind((self.ip, self.port))
        print(
            f'client for incoming socket created: {self.client_sock.getsockname()}')
        self.client_sock.listen(10)  # max connections

        # add client to queue to go to server
        self.client_socket_queue.append(self.client_sock)

    def start_balancer(self):
        while True:
            # put clients into read mode
            read_sockets, write_sockets, error_sockets = select.select(
                self.client_socket_queue, [], [])
            for sock in read_sockets:
                if sock == self.client_sock:  # new connection
                    self.accept_client()  # accept client
                    break
                else:  # message
                    break

    def accept_client(self):
        sockfd, client_address = self.client_sock.accept()  # accept client
        print(
            f'Connected new client: {client_address} to {self.client_sock.getsockname()}')

        # pick a server
        ip_server, port_server = self.pick_server()

        # make connection to the server
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'server socket made & located at: {server_sock.getsockname()}')
        try:
            server_sock.connect(ip_server, port_server)
            print(
                f'client {client_address} connected to server {server_sock.getsockname()}')
        except:
            print(f"Can't connect to server: {sys.exc_info()[0]}")
            sockfd.close()
            print(f'Closing client {client_address}')
            return

        #
    def pick_server(self):
        return self.round_robin(ITERATOR)

    def round_robin(self, iterate):
        return next(iterate)
    # self.client_sock.close()
