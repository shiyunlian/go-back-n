import time, socket

# serverName='172.16.210.4'
serverName='10.0.0.175'
# serverName='127.0.0.1'
#serverName = '10.0.0.81'
host = socket.gethostname()
ip = socket.gethostbyname(host)
PORT = 1234
print(host, "(", ip, ")")

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# initiates the TCP connection between the client and server.
clientSocket.connect((serverName,PORT))

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
clientSocket.send(request.encode())

# receive response from server
response = clientSocket.recv(1024)
print('From Server:' , response.decode())