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

while True:

    message = connectionSocket.recv(1024).decode()
    if(message == 'exit'):
        print("Program terminated.")
        break
    seq_num_range = int(pow(2,int(message))-1)
    win_begin = 0
    ack_message = ""
    message = ""

    while win_begin <= seq_num_range:
        random_num = random.randint(0,99)
        if(random_num == 0):
            ack_message ="ACK Lost"
            message = connectionSocket.recv(1024).decode()
            connectionSocket.send(ack_message.encode())

        else:
            ack_message = "ACK "+str(win_begin)
            message = connectionSocket.recv(1024).decode()
            connectionSocket.send(ack_message.encode())
            win_begin=win_begin+1

connectionSocket.close()