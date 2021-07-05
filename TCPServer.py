import socket,random

# creates the server’s socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
PORT = 1234
serverSocket.bind((host, PORT))
print(host, "(", ip, ")")
     
serverSocket.listen(1)
print("Server is listening...")

while True:
    connectionSocket, addr = serverSocket.accept()
    response = 'success' if connectionSocket.recv(1024).decode() == 'network' else 'failure'
    connectionSocket.send(response.encode())
    print("Established connection from ", addr[0])

    while True:

        message=serverSocket.recv(1024).decode()
        if(message=='exit'):
            print("Program terminated.")
            break
        seq_num_range=pow(2,int(message))-1
        win_begin=0
        ack_message=""
        message=""

        while win_begin!=seq_num_range:
            random_num=random.randint(0,9)
            if(random_num==0):
                ack_message="ACK Lost"
                message = serverSocket.recv(1024).decode()
                serverSocket.send(ack_message.encode())

            else:
                ack_message="ACK "+str(win_begin)
                message = serverSocket.recv(1024).decode()
                serverSocket.send(ack_message.encode())
                win_begin=win_begin+1

    connectionSocket.close()