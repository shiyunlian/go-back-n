import time, socket

# serverName='172.16.210.4'
serverName='10.0.0.175'
# serverName='127.0.0.1'
#serverName = '10.0.0.81'
serverPort = 1234

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# initiates the TCP connection between the client and server.
clientSocket.connect((serverName,serverPort))

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
clientSocket.send(request.encode())

# receive response from server
response = clientSocket.recv(1024)
print('From Server:' , response.decode())

while True:

    message = input(str("Please enter the bits of sequence number or 'exit' to exit the program: "))
    if message == "exit":
        clientSocket.send(message.encode())
        print("Program terminated.")
        break

    # send the message to server
    clientSocket.send(message.encode())

    # calculate the range of sequence number
    seq_num_range=int(pow(2,int(message))-1)
    print("The range of sequence number is 0 to", seq_num_range)
    
    # ask for the window size
    win_size = int(input("Please enter the window size: "))
    if(win_size) < 0:
        print("Invalid window size")
        break
    win_size = win_size - 1
    win_begin = 0
    win_end = win_size

    ack_message = ""

    n=0
    message_list = ""
    while n <= seq_num_range:
        message_list = message_list+str(n)
        n+=1
    print("The sequence number includes:", message_list)

    while win_begin < seq_num_range:
        clientSocket.send(message_list[win_begin].encode())
        ack_message=clientSocket.recv(1024).decode()
        print(ack_message)
        if ack_message != "ACK Lost":
            time.sleep(1)
            if win_end < seq_num_range:
                print("Acknowledgement received! The sliding window is in the range "+str(win_begin+1)+" to "+str(win_end+1)+". Send the next sequence number.")
                win_begin = win_begin + 1
                win_end = win_end + 1
            else:
                print("Acknowledgement received! The sliding window is in the range "+str(win_begin+1)+" to "+str(win_end)+". Send the next sequence number.")
                win_begin = win_begin + 1
                time.sleep(1)
        else:
            time.sleep(1)
            print("Acknowledgement lost! The sliding window remains in the range "+str(win_begin)+" to "+str(win_end)+". Resend the same sequence number.")
            time.sleep(1)

    while win_begin == seq_num_range:
        clientSocket.send(message_list[win_begin].encode())
        ack_message=clientSocket.recv(1024).decode()
        print(ack_message)
        if ack_message != "ACK Lost":
            time.sleep(1)
            print("Acknowledgement received! All the sequence numbers received.")
            win_begin = win_begin + 1
        else:
            time.sleep(1)
            print("Acknowledgement lost! The sliding window remains in the range "+str(win_begin)+" to "+str(win_end)+". Resend the same sequence number.")
            time.sleep(1)

               
    #while win_begin < seq_num_range:
        # while win_begin!=(seq_num_range-win_size):
        #     clientSocket.send(message_list[win_begin].encode())
        #     ack_message=clientSocket.recv(1024).decode()
        #     print(ack_message)
        #     if(ack_message!="ACK Lost"):
        #         time.sleep(1)
        #         print("Acknowledgement received! The sliding window is in the range "+str(win_begin+1)+" to "+str(win_end+1)+". Send the next sequence number.")
        #         win_begin=win_begin+1
        #         win_end=win_end+1
        #         time.sleep(1)
        #     else:
        #         time.sleep(1)
        #         print("Acknowledgement lost! The sliding window remains in the range "+str(win_begin)+" to "+str(win_end)+". Resend the same sequence number.")
        #         time.sleep(1)



        # while(win_begin==seq_num_range):
        #     clientSocket.send(message_list[win_begin].encode())
        #     ack_message=clientSocket.recv(1024).decode()
        #     print(ack_message)
        #     if(ack_message!="ACK Lost"):
        #         time.sleep(1)
        #         print("Acknowledgement received! All the sequence numbers received.")
        #         break
        #     else:
        #         time.sleep(1)
        #         print("Acknowledgement lost! The sliding window remains in the range "+(str(win_begin))+" to "+str(win_end)+". Resend the same sequence number.")

# closes the socket and closes the TCP connection
clientSocket.close()