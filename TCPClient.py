import time, socket

# serverName='172.16.210.4'
# serverName='10.0.0.175'
# serverName='127.0.0.1'
serverName = '10.0.0.81'
serverPort = 1234

clientSocket = socket(AF_INET, SOCK_STREAM)

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
        conn.send(message.encode())
        print("Program terminated.")
        break
    conn.send(message.encode())
    seq_num_range=pow(2,int(message))-1
    print("The range of sequence number is 0 to", seq_num_range)
    
    n=0
    message_list = ""
    while n < seq_num_range:
        message_list= message_list+str(n)
        n+=1
    
    win_size=int(input("Please enter the window size: "))
    win_size=win_size-1
    win_begin=0
    win_end=win_size
    ack_message=""
    
    while win_begin!=seq_num_range:
        while(win_begin!=(seq_num_range-win_size)):
            conn.send(message_list[win_begin].encode())
            ack_message=conn.recv(1024).decode()
            print(ack_message)
            if(ack_message!="ACK Lost"):
                time.sleep(1)
                print("Acknowledgement received! The sliding window is in the range "+(str(win_begin+1))+" to "+str(win_end+1)+". Send the next sequence number.")
                win_begin=win_begin+1
                win_end=win_end+1
                time.sleep(1)
            else:
                time.sleep(1)
                print("Acknowledgement lost! The sliding window remains in the range "+(str(win_begin+1))+" to "+str(win_end+1)+". Resend the same sequence number.")
                time.sleep(1)

        while(win_begin!=seq_num_range):
            conn.send(message_list[win_begin].encode())
            ack_message=conn.recv(1024).decode()
            print(ack_message)
            if(ack_message!="ACK Lost"):
                time.sleep(1)
                print("Acknowledgement received! The sliding window is in the range "+(str(win_begin+1))+" to "+str(win_end)+". Send the next sequence number.")
                win_begin=win_begin+1
                time.sleep(1)
            else:
                time.sleep(1)
                print("Acknowledgement lost! The sliding window remains in the range "+(str(win_begin+1))+" to "+str(win_end)+". Resend the same sequence number.")
                time.sleep(1)

# closes the socket and closes the TCP connection
clientSocket.close()