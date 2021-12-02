# Distributed-Project

Compile the each server file, then loadbreaker, and finally the client file. 

## Set up
1. Make sure you have python 3.8 or higher
2. Clone this repo
3. Open the folder you cloned
4. Open 6 terminals in this folder

## To Run
1. First, Run the servers in each terminal `python Server<#>.py` where <#> is 1,2,3,4
2. Next, run the load balancer in another terminal `python LoadBalancer.py`
3. Finally, run the client in another terminal `python Client.py`
