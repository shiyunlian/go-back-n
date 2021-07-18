# Go Back N ARQ. Server Side Code
#Assume Receiver to continuously receive frames w/o awaiting sender timeout for a particular window
import socket
import random

# get the hostname
host = socket.gethostname()
port = 1234  # initiate port no above 1024
exp = 0
last_recieved = -1
n = 4
sent_complete = False
packet_reieved = 0
packet_num = 10000000
packet_resent = 0
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)
conn, address = server_socket.accept()  # accept new connection
print ("Connection from: ", str(address))
print ("packet number is ", packet_num)

while True:
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024).decode()
    if not data:
        # if data is not received break
        break
    
    rec = int(data)
    count = 0
    flag = 0       

    while(count!=n and rec <= packet_num):

        print ("Incoming Frame -> ", rec, "    Expected Frame -> ", exp)

        if rec != exp:
            print ("Out of order! Discard Frame  -> ", rec)
            packet_reieved += 1
            packet_resent += 1
            flag = 1
            break
        elif random.random() < 0.1:
            print ("Lost Frame  -> ", rec)
            flag = 1
            packet_resent += 1
            break
        elif rec == exp:
            print ("Received Frame -> ", rec)
            count += 1
            exp += 1
            rec += 1
            packet_reieved += 1
            if rec > packet_num:
                sent_complete = True
            continue
        else:
            break

    if(flag == 1):
        last_recieved = exp - 1
        ack = last_recieved
        if n > 4:
            n = int(n / 2)
            print("Adjust window size from " + str(int(2*n)) + " to " + str(n))
        else:
            print("Window size remains to be 4")
    elif sent_complete:
        ack = int(rec)
    else:
        ack = int(data)+n-1
        if n < 256:
            n = int(2 * n)
            print("Adjust window size from " + str(int(n/2)) + " to " + str(n))
        else:
            print("Window size remains to be 256")

    print("Sending Ack ", ack)
    print ('***************************************************')
    data=str(ack)
    conn.send(data.encode())  # send data to the client
    
print("Recieved total packets: ", packet_reieved)
print("Resent total packets: ", packet_resent)
conn.close()  # close the connection