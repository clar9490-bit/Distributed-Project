import socket
import select

HOST = '127.0.0.1'
PORT = 1002


def close_client(socket):
    print(f"closing client {socket.getpeername()}")
    socket.send("you may not enter".encode())
    socket.close()


if __name__ == '__main__':

    # define a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # set options, bind socket to ip:port and listen on that address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)  # take max 10 connections
    print(f'socket listening on {server_socket.getsockname()}')

    while True:
        client, info = server_socket.accept()
        print(f'Got a connection from {(info)}')

        client.send(
            "Are you vaccinated against COVID-19?\nDo you have any COVID-19 symptoms?".encode())
        # Q1: Are u vaxx
        # Q2: Do u have covid19 symptoms
        q = client.recv(1024).decode()
        answers = q.split()
        if answers[0] == 'NO' or answers[1] == 'YES':
            close_client(client)
        else:
            print(f'Allowing client-{info} to enter')
            client.send("You may ENTERRR".encode())
