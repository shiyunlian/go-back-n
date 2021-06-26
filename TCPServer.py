from socket import *
serverPort = 12000

# creates the server’s socket
serverSocket = socket(AF_INET,SOCK_STREAM)

#associate the server port number with server socketß
serverSocket.bind(('',serverPort))

#the server listen for TCP connection requests from the client. 
# The parameter specifies the maximum number of queued connections (at least 1).
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()