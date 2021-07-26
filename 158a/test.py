import socket, random, time
import matplotlib.pyplot as plt

# get the hostname and ip
host = socket.gethostname()
ip = socket.gethostbyname(host)
print(host, "ip address: ", ip)