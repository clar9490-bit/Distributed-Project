import socket
import time
import random

time_per_client = []

options = ['YES', 'NO']


# def check_answer(msg, client):
#     if msg == "You may NEVER ENTERRR":
#         print(msg)
#         client.close()


total_start = time.time()
for i in range(10):
    s = time.time()  # start timer per client

    # connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1005))

    # q1
    msg = client.recv(4096).decode("utf-8")
    # check_answer(msg, client)
    print(msg)

    answer = random.choice(options)
    answer = answer + ' ' + random.choice(options)  # select random choice
    print(answer)

    client.send(answer.encode())

    serverResponse = client.recv(4096).decode("utf-8")
    print(serverResponse)

    # stop timer per client
    e = time.time()
    time_per_client.append(e-s)

print(f'Total time: {time.time()-total_start}')
print(f'Avg time per client: {sum(time_per_client)/len(time_per_client)}')
