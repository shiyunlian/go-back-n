import socket
PORT = 1234
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',PORT))
print('Server is ready to listen')

try:
    serverSocket.listen(10)
    print('Server is listening...')
except:
    print('Server is not listening...')
