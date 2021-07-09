import socket,random,sys
from struct import *

# creates the server’s socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
PORT = 1234
serverSocket.bind((host, PORT))
print(host, "(", ip, ")")

# server listens for connection
try:
    serverSocket.listen(1)
    print('Server is listening...')
except:
    print('Server is not listening...')

# server establishes incoming connection
try:
    connectionSocket, addr = serverSocket.accept()
    response = 'success' if connectionSocket.recv(1024).decode() == 'network' else 'failure'
    connectionSocket.send(response.encode())
    print("Established connection from ", addr[0])
except:
    print("Connection failed")

packet_receive = 0
prob_lost = 0.01
last_receive = -1
# received = []
# received_buffer = []

# for i in range(win_size):
#     received.append(0)
#     received_buffer.append(None)

ack_message = ""
message = ""

while True:
    # receive the first byte of packet
    seq_num = int(connectionSocket.recv(1024).decode())

    # if random.random() > prob_lost, packet received, else packet lost, count the received packets
    if random.random() > prob_lost:
        print("Received packet ", seq_num)
        packet_receive = packet_receive + 1

        # if packet num matches receiver num, receiver sends Ack #, updates last_receive by increment 1
        if seq_num == last_receive + 1:
            print("Sent Ack ", seq_num)
            #ack_message = "ACK " + str(seq_num)
            #connectionSocket.send(ack_message.encode())
            connectionSocket.send(str(seq_num).encode())
            last_receive = seq_num

        elif seq_num != last_receive + 1 and seq_num > last_receive + 1:
            if last_receive >= 0:
                print("Packet out of order and discarded. Last received packet in order is packet" + str(last_receive))
                #ack_message = "ACK " + str(last_receive)
                #connectionSocket.send(ack_message.encode())
                connectionSocket.send(str(last_receive).encode())

        # else:
        #     print("Sent Ack ", seq_num)
        #     ack_message = "ACK " + str(seq_num)
        #     connectionSocket.send(ack_message.encode())
        #     last_receive = seq_num

    else:
        print("Packet" + seq_num + "lost.")
        # if last_receive == -1:
        #     ack_message = "Packet 0 lost"
        # else:
        # ack_message = "ACK " + str(last_receive)
        # connectionSocket.send(ack_message.encode())
        connectionSocket.send(str(last_receive).encode())

    # while win_begin <= win_size:
    #     random_num = random.randint(0,99)
    #     if(random_num == 0):
    #         ack_message ="ACK Lost"
    #         message = connectionSocket.recv(1024).decode()
    #         connectionSocket.send(ack_message.encode())

    #         if win_size > 1:
    #             win_size = win_size / 2
    #     else:
    #         ack_message = "ACK "+str(win_begin)
    #         message = connectionSocket.recv(1024).decode()
    #         connectionSocket.send(ack_message.encode())
    #         win_begin = win_begin + 1

    #         # limit maximum window size
    #         if win_size <= 256:
    #             win_size = win_size * 2
