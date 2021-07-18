# Go Back N. Server Side Code
# Assume Receiver to continuously receive packets w/o awaiting sender timeout for a particular window
import socket, random, time

# get the hostname and ip
host = socket.gethostname()
ip = socket.gethostbyname(host)
print(host, "ip address: ", ip)

# create a socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
port = 1234

# bind host address and port together
server_socket.bind((host, port))  

# configure how many client the server can listen simultaneously
try:
    server_socket.listen(10)
    print('Server is listening...')
except:
    print('Server is not listening...')

# try to establish connection and send response back to client
try:
    conn, address = server_socket.accept()  
    response = 'success' if conn.recv(1024).decode() == 'network' else 'failure'
    conn.send(response.encode())
    print("Established connection from ", str(address))
except:
    print("Connection failed")

# expected packet to be received
expected_packet = 0

# minimun window size
win_size = 4 
rest_window_size = 0

# indicate if every 65535 packets are sent successfully
sent_complete = False
packets_sent_complete = False
limit = 100

# indicate if there is packet dropped or out of order
flag = 0
last_packet = -1

# total packets to be sent
packet_num = 1000 - 1 
resent_packets = 0
resent_packets_buffer = [] # an array to store resent packets every 1000 packets received
receive_packets = 0
receive_packets_buffer =[] # an array to store packets received in order
sent_packets = 0
sent_packets_buffer =[] # an array to store # of sent packets every 1000 packets received
countdown = int(packet_num / limit) + 1
good_put = [] # an array to store good_put every 1000 packets received
avg_good_put = 0 
last_received_packet = [] # an array to store the last received packets if the next packet is dropped
time_buffer = []

# shrink window size to half if packet is dropped
def ShrinkWindowSize():
    global win_size
    if win_size > 4:
        win_size = int(win_size / 2)
        print("Adjust window size from " + str(int(2 * win_size)) + " to " + str(win_size))
    else:
        print("Window size remains to be 4")

# expand window size twice if no packet is dropped
def ExpandWindowSize():
    global win_size
    if win_size < 256:
        win_size = int(2 * win_size)
        print("Adjust window size from " + str(int(win_size/2)) + " to " + str(win_size))
    else:
        print("Window size remains to be 256")

# handle lost or out of order packet
def HandleLostPacket():
    global last_packet, last_received , expected_packet, flag
    last_packet = expected_packet - 1
    last_received_packet.append(last_packet)
    flag = 1

# calculate avg good put
def CalculateAvgGoodPut():
    global good_put, avg_good_put
    i = 0
    sum = 0
    while i < len(good_put):
        sum = good_put[i] + sum
        i += 1
    avg_good_put = sum / len(good_put)
    return avg_good_put

# calculate total number of sent packets
def CalculateSentPackets():
    global sent_packets, sent_packets_buffer
    i = 0
    while i < len(sent_packets_buffer):
        sent_packets = sent_packets_buffer[i] + sent_packets
        i += 1
    return sent_packets

# calculate total number of resent packets
def CalculateResentPackets():
    global resent_packets, receive_packets_buffer
    i = 0
    while i < len(resent_packets_buffer):
        resent_packets = receive_packets_buffer[i] + resent_packets
        i += 1
    return resent_packets

# start the time
start_time = time.time()
while True:
    
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024).decode()
    
    # if data is not received break
    if not data:
        break

    data = int(data)
    if data > limit:
        data = (data - 1) % limit
    recent_packet = data
    count = 0   
    last_received = []
    flag = 0

    while(count != win_size and recent_packet  <= limit):

        # if expected_packet > limit:
        #     expected_packet = 0

        print ("Incoming Packet -> ", recent_packet , "    Expected Packet -> ", expected_packet)
        sent_packets += 1
        time.sleep(0.1)

        # check if the packet is out of order
        if recent_packet  != expected_packet:
            print ("Out of order! Discard Packet  -> ", recent_packet )
            HandleLostPacket()

        # check if the packet is lost
        elif random.random() < 0.01:
            print ("Lost Packet  -> ", recent_packet )
            HandleLostPacket()
            count += 1
            recent_packet += 1
            expected_packet += 1
        
        # if recent_packet is expected_packet, add to the receive_packets_buffer, increment expected_packet, 
        # check if the packet reaches limit, if yes, set sent_complete to be true, set expected_packet to be 0
        # if not, increment recent_packet and expected_packet
        elif recent_packet == expected_packet:
            print ("Received Packet -> ", recent_packet )
            count += 1
            receive_packets_buffer.append(recent_packet)
            if recent_packet == limit:
                sent_complete = True
                expected_packet = 0
                rest_window_size = win_size - count
                break
            else:
                sent_complete = False
                recent_packet += 1
                expected_packet += 1
        else:
            break
        
        # calculate good_put every 1000 packets received
        if len(receive_packets_buffer) == 1000:
            receive_packets = 1000 + receive_packets
            resent_packets_buffer.append(1000-len(sorted(set(receive_packets_buffer))))
            good_put.append(len(receive_packets_buffer)/sent_packets)
            sent_packets_buffer.append(sent_packets)
            receive_packets_buffer = []
            sent_packets = 0

    # if there are packets dropped, send the last received packet cumulative ack and shrink window size
    if flag == 1:
        ack = last_received_packet[0]
        expected_packet = last_received_packet[0]+1
        ShrinkWindowSize()
        last_received_packet = []

    # if the packet reaches the limit, send the ack
    elif sent_complete:
        ack = int(recent_packet)
        countdown -= 1
        sent_complete = False
        
    # if all the packets are acknowledged, send cumulative ack and expand window size
    else:
        ack = int(data) + win_size - 1
        ExpandWindowSize()

    if  countdown >= 0:
        print("Sending Ack ", ack)
        print ('***************************************************')
        data = str(ack)
        # send Ack number to the client
        conn.send(data.encode()) 

    else:
        break

# check if there are any packets left in the buffer
if receive_packets_buffer:
    receive_packets = len(receive_packets_buffer) + receive_packets
    resent_packets_buffer.append(len(receive_packets_buffer)-len(sorted(set(receive_packets_buffer))))
    good_put.append(len(receive_packets_buffer)/sent_packets)

# end time and calculate elapsed_time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
print("Sent total packets: ", CalculateSentPackets())
print("Received total packets: ", receive_packets)
print("Resent total packets: ", CalculateResentPackets())
print("Good-put: ", CalculateAvgGoodPut())

# close the connection
conn.close()  