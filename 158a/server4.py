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

# configure how many clients the server can listen simultaneously
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

# minimun window size is 1, maximum window size is 256
win_size = 1
win_size_buffer = [] # an array to keep track of window size changes
win_size_time = []  # an array to keep track of the time when window size changes 

# indicate if every 65535 packets are sent successfully
sent_complete = False
limit = 1000

# indicate if there is packet dropped or out of order
is_packet_lost = False
is_first_packet_lost = False
is_last_packet_received = False
last_packet = -1 

# total packets to be sent
packet_num = 1021

resent_packets = 0
resent_packets_buffer = [] # an array to store resent packets every 1000 packets received

receive_packets = 0
receive_packets_buffer =[] # an array to store packets received in order

sent_packets = 0
sent_packets_buffer =[] # an array to store # of sent packets every 1000 packets received

countdown = int(packet_num / limit) +1# a counter to keep track of every 65535 packets out of 10,000,000 packets

avg_good_put = 0 
good_put = [] # an array to store good_put 
good_put_time_buffer = [] # an array to keep track of every 1000 packets received

last_received_packet = [] # an array to store the last received packets if the next packet is dropped

lost_packets_buffer = []    # an array to store the lost packets
lost_packets_time_buffer = []   # an array to keep track of the time when packets are lost

track_packet_num_buffer = []    # an array to keep track of packet received number
track_packet_num_time_buffer = []   # an array to keep track of packet received time

last_ack_sent = packet_num % limit - 1# calculate the last ack sent based on the packet number and sequence number limit

all_packets_received = False
track_packet_sent_times_buffer = []    # an array to keep track of how many times each packet sent
track_packet_sent_buffer = []
buffer =[]
packets_resent_times = []

# shrink window size to half if packet is dropped
def ShrinkWindowSize(): 
    global win_size, win_size_buffer, win_size_time
    win_size_time.append(round(time.time() - start_time, 1))
    if win_size > 1:
        win_size = int(win_size / 2)
        print("Adjust window size from " + str(int(2 * win_size)) + " to " + str(win_size))
    else:
        print("Window size remains to be 4")
    win_size_buffer.append(win_size)

# expand window size twice if no packet is dropped
def ExpandWindowSize():
    global win_size, win_size_buffer
    win_size_time.append(round(time.time() - start_time, 1))
    if win_size < 128:
        win_size = int(2 * win_size)
        print("Adjust window size from " + str(int(win_size/2)) + " to " + str(win_size))
    else:
        print("Window size remains to be 128")
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
    sent_packets = 0
    i = 0
    while i < len(sent_packets_buffer):
        sent_packets = sent_packets_buffer[i] + sent_packets
        i += 1
    return sent_packets

# calculate total number of resent packets
def CalculateResentPackets():
    global resent_packets, resent_packets_buffer, packet_num
    resent_packets = 0
    #resent_packets = CalculateSentPackets() - packet_num
    #return resent_packets
    i = 0
    while i < len(resent_packets_buffer):
        resent_packets = resent_packets_buffer[i] + resent_packets
        i += 1
    return resent_packets

# keep track of the number and the time of packets received 
def TrackReceivedPackets():
    global receive_packets,receive_packets_buffer,track_packet_num_buffer,track_packet_num_time_buffer
    receive_packets += 1
    receive_packets_buffer.append(recent_packet)
    track_packet_num_buffer.append(recent_packet)
    track_packet_num_time_buffer.append(round(time.time()-start_time,1))

# keep track of how many times of each packets to be sent every 65535
def TrackSentPackets():
    global track_packet_sent_buffer, track_packet_sent_times_buffer, buffer
    track_packet_sent_times_buffer = []
    buffer = []
    i = 0
    if countdown != 1:
        while i < limit:
            track_packet_sent_times_buffer.append(track_packet_sent_buffer.count(i))
            i += 1

    if countdown == 1:
        for i in range(len(track_packet_sent_buffer)):
            track_packet_sent_times_buffer.append(track_packet_sent_buffer.count(i))
    # print(len(track_packet_sent_buffer))
    # print(len(track_packet_sent_times_buffer))
    # print(track_packet_sent_buffer)
    # print(track_packet_sent_times_buffer)
    for i in range(0,10):
        buffer.append(track_packet_sent_times_buffer.count(i))

    for i in range(0,10):
        packets_resent_times[i] = packets_resent_times[i] + buffer[i]

    track_packet_sent_buffer = []

# start the timer
start_time = time.time()
win_size_time.append(0)
win_size_buffer.append(win_size)
print("countdown: ", countdown)
sent = 0
received = 0
lost = 0
for i in range(0,10):
    packets_resent_times.append(0)

while countdown > 0 and all_packets_received == False:

    counter = 0
    last_received_packet = []

    # if is_last_packet_received:
    #     countdown = 0
    #     break

    while counter < win_size and all_packets_received == False:

        # get the packets from client
        recent_packet = conn.recv(1024).decode()
        
        if not recent_packet:
            countdown = 0
            break

        recent_packet = int(recent_packet)
 
        if recent_packet >= limit:
            recent_packet = recent_packet % limit

        sent_packets += 1
        sent += 1
        track_packet_sent_buffer.append(recent_packet)
        # if recent_packet != limit - 1:
            

        # if random.random() > 0.01, increment receive_packets, append the packet into receive_packets_buffer and tracket_packet_num_buffer
        if random.random() >= 0.01:
            received += 1
            if countdown == 1 and recent_packet == last_ack_sent and is_packet_lost == False:
                print("Received the last packet ", recent_packet, ". All the packets have been received")
                TrackReceivedPackets()
                all_packets_received = True
                # TrackSentPackets()
                # print(packets_resent_times)
                break

            elif countdown == 1 and recent_packet == last_ack_sent and is_packet_lost == True:
                print("Received packet ", recent_packet, " Expected packet ", expected_packet)
                TrackReceivedPackets()
                is_last_packet_received = True
                break

            else:
                TrackReceivedPackets()

            # calculate good_put every 1000 packets received
            if len(receive_packets_buffer) == 1000:
                CalculateGoodPut()

            # check if received packet is expected
            if recent_packet == expected_packet:
                print("Received packet ", recent_packet, " Expected packet ", expected_packet)

                # check if received packet reaches limit
                if recent_packet == limit - 1:
                    # track_packet_sent_buffer.append(recent_packet)
                    # print(len(track_packet_sent_buffer))
                    # TrackSentPackets()
                    # print(packets_resent_times)
                    sent_complete = True
                    expected_packet = 0
                    break
                else:
                    sent_complete = False
                    expected_packet += 1

            else:
                print ("Received packet ", recent_packet, " Expected packet ", expected_packet, "Out of order packet", recent_packet )
                HandleLostPacket()
        
        # if the packet is lost, append the lost packet to lost_packets_buffer and keep track of the time
        else:
            lost += 1
            print ("Lost packet", recent_packet )
            lost_packets_buffer.append(recent_packet)
            lost_packets_time_buffer.append(round(time.time()-start_time,1))

            # if the lost packet reaches limit, then set ack to be previous recent_packet number and break the loop
            if recent_packet == limit-1: # since packet num starts from 1, the last packet num will be limit - 1
                HandleLostPacket()
                break

            # if the lost packet is the first packet, then handle lost packet
            elif recent_packet == 0:
                HandleLostPacket()
                is_first_packet_lost = True
                break
            else:
                HandleLostPacket()

        counter += 1

    if all_packets_received:
        TrackSentPackets()
        print(packets_resent_times)
        print("Sending last Ack ", last_ack_sent)
        print ('*******************************************')
        ack = str(last_ack_sent)

        # send Ack number to the client
        conn.send(ack.encode()) 
        break

    # if last packet is received but there is packet lost
    elif is_last_packet_received:
        ack = last_received_packet[0]
        expected_packet = last_received_packet[0]+1
        is_packet_lost = False
        is_last_packet_received = False

    # if there are packets dropped, send the last received packet cumulative ack and shrink window size
    elif is_first_packet_lost and countdown == int(packet_num / limit) + 1:
        ack = -1
        is_first_packet_lost = False
        is_packet_lost = False

    elif is_first_packet_lost and countdown != int(packet_num / limit) + 1:
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

    # if the packet reaches the limit, send the ack of the limit/recent_packet, track sent packets, expand window size
    elif sent_complete:
        ack = recent_packet
        TrackSentPackets()
        print(packets_resent_times)
        countdown -= 1
        print("Countdown left:", countdown)
        sent_complete = False
        ExpandWindowSize()

    # if all the packets are acknowledged, send cumulative ack and expand window size
    else:
        ack = recent_packet
        ExpandWindowSize()
        if expected_packet >= limit:
            expected_packet = 0

    # send Ack number to the client
    if  countdown >= 0:
        print("Sending Ack ", ack)
        print ('***************************************************')
        ack = str(ack)
        conn.send(ack.encode()) 
    else:
        break

# check if there are any packets left in the receive_packets_buffer
if receive_packets_buffer:
    CalculateGoodPut()

# end time and calculate elapsed_time
end_time = time.time()

# print("Elapsed time: ", round(end_time - start_time, 2))
print("Sent total packets:", CalculateSentPackets(), sent)
print("Received total packets:", receive_packets, received)
print("Lost total packets:", len(lost_packets_buffer), lost)
print("Resent total packets: ", CalculateResentPackets(), sent - packet_num)
# print("Average good-put: ", CalculateAvgGoodPut())
# print("Good-put: ", good_put)
# print("Good-put time interval: ", good_put_time_buffer)
# print("Window size: ", win_size_buffer)
# print("Window size time interval: ", win_size_time)
# print("Lost packets:", lost_packets_buffer)
# print("Lost packets time interval:", lost_packets_time_buffer)
# print("Track received packets num:", track_packet_num_buffer)
# print("Track received packets num time:", track_packet_num_time_buffer)


print("packet resent time 1:", packets_resent_times[2])
print("packet sent time 2:", packets_resent_times[3]*2)
print("packet sent time 3:", packets_resent_times[4]*3)
print("packet sent time 4:", packets_resent_times[5]*4)
print("resent packets:",packets_resent_times[2]+packets_resent_times[3]*2+packets_resent_times[4]*3+packets_resent_times[5]*4)

# close the connection
conn.close()  