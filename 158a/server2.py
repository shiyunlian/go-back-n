import socket, random, time

# get the hostname and ip
host = socket.gethostname()
ip = socket.gethostbyname(host)
print(host, "ip address: ", ip)

# create a socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
port = 12340

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
win_size_buffer = []
win_size_time = []
rest_window_size = 0

# indicate if every 65535 packets are sent successfully
sent_complete = False
limit = 100

# indicate if there is packet dropped or out of order
is_packet_lost = False
is_first_packet_lost = False
last_packet = -1

# total packets to be sent
packet_num = 1500
resent_packets = 0
resent_packets_buffer = [] # an array to store resent packets every 1000 packets received
receive_packets = 0
receive_packets_buffer =[] # an array to store packets received in order
sent_packets = 0
sent_packets_buffer =[] # an array to store # of sent packets every 1000 packets received
countdown = int(packet_num / limit) 
good_put = [] # an array to store good_put every 1000 packets received
avg_good_put = 0 
last_received_packet = [] # an array to store the last received packets if the next packet is dropped
good_put_time_buffer = []
start_time = time.time()
lost_packets_buffer = []
lost_packets_time_buffer = []


# shrink window size to half if packet is dropped
def ShrinkWindowSize():
    global win_size, win_size_buffer, win_size_time
    win_size_time.append(round(time.time() - start_time, 1))
    if win_size > 4:
        win_size = int(win_size / 2)
        print("Adjust window size from " + str(int(2 * win_size)) + " to " + str(win_size))
    else:
        print("Window size remains to be 4")
    win_size_buffer.append(win_size)

# expand window size twice if no packet is dropped
def ExpandWindowSize():
    global win_size, win_size_buffer
    win_size_time.append(round(time.time() - start_time, 1))
    if win_size < 256:
        win_size = int(2 * win_size)
        print("Adjust window size from " + str(int(win_size/2)) + " to " + str(win_size))
    else:
        print("Window size remains to be 256")
    win_size_buffer.append(win_size)

# handle lost or out of order packet
def HandleLostPacket():
    global last_packet, last_received_packet, expected_packet, is_packet_lost
    is_packet_lost = True
    if expected_packet > 0:
        last_packet = expected_packet - 1
    else:
        last_packet = limit
    last_received_packet.append(last_packet)

    if expected_packet < limit:
        expected_packet += 1
    else:
        expected_packet = 0

# calculate good_put every 1000 packets received
def CalculateGoodPut():
    global receive_packets_buffer, good_put_time_buffer, receive_packets, resent_packets_buffer, good_put, sent_packets_buffer, sent_packets
    good_put_time_buffer.append(round(time.time() - start_time, 1))
    resent_packets_buffer.append(len(receive_packets_buffer)-len(sorted(set(receive_packets_buffer))))
    good_put.append(len(receive_packets_buffer)/sent_packets)
    print("Good-put:", len(receive_packets_buffer)/sent_packets)
    sent_packets_buffer.append(sent_packets)
    receive_packets_buffer = []
    sent_packets = 0

# calculate avg good put
def CalculateAvgGoodPut():
    global good_put, avg_good_put
    i = 0
    sum = 0
    while i < len(good_put):
        sum = good_put[i] + sum
        i += 1
    avg_good_put = sum / len(good_put)
    return round(avg_good_put, 2)

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
    global resent_packets, resent_packets_buffer
    i = 0
    while i < len(resent_packets_buffer):
        resent_packets = resent_packets_buffer[i] + resent_packets
        i += 1
    return resent_packets


win_size_buffer.append(win_size)
win_size_time.append(0)
while countdown > 0:
    
    # receive data stream. it won't accept data packet greater than 1024 bytes
    counter = 0
    is_packet_lost = 0
    last_received_packet = []

    while counter < win_size:

        # get the packets from client
        recent_packet = conn.recv(1024).decode()
        
        if not recent_packet:
            break
        
        recent_packet = int(recent_packet)
        if recent_packet >= limit:
            recent_packet = recent_packet % limit
 
        sent_packets += 1

        # if random.random() > 0.01, append the packet into buffer
        if random.random() >= 0.01:
            receive_packets += 1
            receive_packets_buffer.append(recent_packet)

            if len(receive_packets_buffer) == 100:
                CalculateGoodPut()

            # check if received packet is expected
            if recent_packet == expected_packet:
                print("Received packet ", recent_packet, " Expected packet ", expected_packet)
                # check if received packet reaches limit
                if recent_packet == limit - 1:
                    sent_complete = True
                    expected_packet = 0
                    break
                else:
                    sent_complete = False
                    expected_packet += 1

            else:
                print ("Received packet ", recent_packet, " Expected packet ", expected_packet, "Out of order packet", recent_packet )
                HandleLostPacket()
        
        # check if the packet is lost
        else:
            print ("Lost packet", recent_packet )
            lost_packets_buffer.append(recent_packet)
            lost_packets_time_buffer.append(round(time.time()-start_time,1))
            if recent_packet == limit - 1:
                ack = recent_packet - 1
                break
            elif recent_packet == 0:
                HandleLostPacket()
                is_first_packet_lost = True
                break
            else:
                HandleLostPacket()
         
         # calculate good_put every 1000 packets received
        

        counter += 1

    # if there are packets dropped, send the last received packet cumulative ack and shrink window size
    if is_first_packet_lost and countdown == int(packet_num / limit):
        ack = -1
        is_first_packet_lost = False
        is_packet_lost = False


    elif is_first_packet_lost and countdown != int(packet_num / limit):
        if last_received_packet:
            ack = last_received_packet[0]
        else:
            ack = limit - 1
        is_first_packet_lost = False
        is_packet_lost = False

    elif is_packet_lost:
        ack = last_received_packet[0]
        expected_packet = last_received_packet[0]+1
        last_received_packet = []
        ShrinkWindowSize()
        if expected_packet >= limit:
            expected_packet = 0
        is_packet_lost = False

    # if the packet reaches the limit, send the ack
    elif sent_complete:
        ack = recent_packet
        countdown -= 1
        print("Countdown", countdown)
        sent_complete = False
        ExpandWindowSize()

    # if all the packets are acknowledged, send cumulative ack and expand window size
    else:
        ack = recent_packet
        ExpandWindowSize()
        if expected_packet >= limit:
            expected_packet = 0

    if  countdown >= 0:
        print("Sending Ack ", ack)
        print ('***************************************************')
        ack = str(ack)

        # send Ack number to the client
        conn.send(ack.encode()) 

    else:
        break

# check if there are any packets left in the buffer
if receive_packets_buffer:
    CalculateGoodPut()

# end time and calculate elapsed_time
end_time = time.time()

print("Elapsed time: ", round( end_time - start_time, 2))
print("Sent total packets: ", CalculateSentPackets())
print("Received total packets: ", receive_packets)
print("Resent total packets: ", CalculateSentPackets()-packet_num)
print("Average good-put: ", CalculateAvgGoodPut())
print("Good-put: ", good_put)
print("Good-put time interval: ", good_put_time_buffer)
print("Window size: ", win_size_buffer)
print("Window size time interval: ", win_size_time)
print("Lost packets:", lost_packets_buffer)
print("Lost packets time interval:", lost_packets_time_buffer)


# close the connection
conn.close()  