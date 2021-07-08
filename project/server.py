import socket,random

# creates the server’s socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
PORT = 1234
serverSocket.bind((host, PORT))
print(host, "(", ip, ")")
     
try:
    serverSocket.listen(1)
    print('Server is listening...')
except:
    print('Server is not listening...')

try:
    connectionSocket, addr = serverSocket.accept()
    response = 'success' if connectionSocket.recv(1024).decode() == 'network' else 'failure'
    connectionSocket.send(response.encode())
    print("Established connection from ", addr[0])
except:
    print("Connection failed")

# while True:
    