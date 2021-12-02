import socket
import time
import random

time_per_client = []
options = ['YES', 'NO']

# start timer for whole run
total_start = time.time()

for i in range(100):  # change this number to the number of clients u want to simulate

    s = time.time()  # start timer per client

    # connect to a server through the load balancer
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1005))

    # get questions
    msg = client.recv(4096).decode("utf-8")
    # print(msg)

    # answer questions
    answer = random.choice(options)
    answer = answer + ' ' + random.choice(options)  # select random choice
    # print(answer)

    # send answer
    client.send(answer.encode())

    # check if allowed in building
    serverResponse = client.recv(4096).decode("utf-8")
    print(serverResponse)

    # stop timer per client
    e = time.time()
    time_per_client.append(e-s)

# print times
print(f'Total time: {time.time()-total_start}')
print(f'Avg time per client: {sum(time_per_client)/len(time_per_client)}')
