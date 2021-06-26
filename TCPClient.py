from socket import *
# serverName = ’servername’
serverName='172.16.210.4'
# serverName='10.0.0.175'
# serverName='127.0.0.1'
serverPort = 12000

# creates the client’s socket,the first parameter indicates the underlying network is using IPv4. 
# The second parameter indicates that the socket is a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiates the TCP connection between the client and server.
clientSocket.connect((serverName,serverPort))

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
clientSocket.send(request.encode())

# receive response from server
response = clientSocket.recv(1024)
print('From Server:' , response.decode())

# closes the socket and closes the TCP connection
clientSocket.close()