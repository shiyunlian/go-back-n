from socket import *
serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

try:
    serverSocket.listen(10)
    print('success')
except:
    print('failure')
    