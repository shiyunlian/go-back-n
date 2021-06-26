from socket import *
serverPort = 12000

# creates the server’s socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# associate the server port number with server socket
serverSocket.bind(('',serverPort))

# the server listen for TCP connection requests from the client. 
# The parameter specifies the maximum number of queued connections (at least 1).
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    response = 'success' if connectionSocket.recv(1024).decode() == 'network' else 'failure'
    connectionSocket.send(response.encode())
    connectionSocket.close()