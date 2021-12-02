import socket
import select
from itertools import cycle

HOST = '127.0.0.1'
PORT = 1005

SERVER_POOL = [('127.0.0.1', 1001), ('127.0.0.1', 1002),
               ('127.0.0.1', 1003), ('127.0.0.1', 1004)]
ITERATOR = cycle(SERVER_POOL)

in_queue = []
out_queue = []
lookup = {}

msg = {}


def start_balancer():
    while True:
        # put clients into read mode
        read_sockets, write_sockets, error_sockets = select.select(
            in_queue, out_queue, [])
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
        for sock in write_sockets:
            if len(out_queue) != 0:
                send(sock)
            else:
                close_socket(sock)


def accept_client():
    sockfd, client_address = client_sock.accept()  # accept client
    sockfd.setblocking(0)
    print(
        f'Connected new client: {client_address} to {client_sock.getsockname()}')

    # pick a server
    ip_server, port_server = round_robin(ITERATOR)

    # make connection to the server
    print(f'server socket located at: {(ip_server, port_server)}')

    client_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_server_sock.connect((ip_server, port_server))
    print(f'client {client_address} connected to server {sockfd.getsockname()}')

    in_queue.append(sockfd)
    in_queue.append(client_server_sock)

    lookup[sockfd] = client_server_sock
    lookup[client_server_sock] = sockfd


def round_robin(iterate):
    return next(iterate)


def receive(replyer: socket.socket, data):
    print(f'{replyer.getpeername()} sent {replyer.getsockname()}: {[data]}')
    requester = lookup[replyer]  # find requester

    msg[requester] = data  # get data to send requester
    out_queue.append(requester)  # add message to out queue
    in_queue.remove(replyer)  # mark message as read


def send(sender):
    data = msg[sender]  # get the data to be sent
    sender.send(data)  # sender sends message

    receiver = lookup[sender]  # get receiver

    in_queue.append(receiver)  # add receiver to in queue
    out_queue.remove(sender)  # remove sent message from queue
    del msg[sender]  # remove data from msg


def close_socket(socket: socket.socket):
    server_socket = lookup[socket]
    in_queue.remove(socket)
    in_queue.remove(server_socket)
    if socket in out_queue:
        out_queue.remove(socket)

    print(f'client {socket.getpeername()} disconnected')

    socket.close()
    server_socket.close()
    del lookup[socket]
    del lookup[server_socket]
    if socket in msg:
        del msg[socket]


client_sock = None
if __name__ == '__main__':
    # make a socket for the incoming client
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sock.bind((HOST, PORT))
    client_sock.setblocking(0)
    print(
        f'listening on: {client_sock.getsockname()}')
    client_sock.listen(10)  # max connections

    # add client to queue to go to server
    in_queue.append(client_sock)
    start_balancer()
