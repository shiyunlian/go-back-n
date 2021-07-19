import socket, random, time
import matplotlib.pyplot as plt
# get the hostname and ip
host = socket.gethostname()
ip = socket.gethostbyname(host)
print(host, "ip address: ", ip)

# create a socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
port = 12340

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

# minimun window size is 1, maximum window size is 128
win_size = 1
win_size_buffer = [] # an array to keep track of window size changes
win_size_time_buffer = []  # an array to keep track of the time when window size changes 

# indicate if every 65535 packets are sent successfully
sent_complete = False
limit = 65536

# indicate if there is packet dropped or out of order
is_packet_lost = False
is_first_packet_lost = False
is_last_packet_received = False
last_packet = -1 

# total packets to be sent
packet_num = 100000

receive_packets = 0     # a counter to keep track of number of packets receive 
receive_packets_buffer =[] # an array to store packets received in order

sent_packets = 0    # a counter to keep track of number of packets sent
sent_packets_buffer =[] # an array to store # of sent packets every 1000 packets received

countdown = int(packet_num / limit) +1# a counter to keep track of every 65535 packets out of 10,000,000 packets

avg_good_put = 0 
good_put = [] # an array to store good_put 
good_put_time_buffer = [] # an array to keep track of every 1000 packets received

last_received_packet = [] # an array to store the last received packets if the next packet is dropped

lost_packets_buffer = []    # an array to store the lost packets
lost_packets_time_buffer = []   # an array to keep track of the time when packets are lost

out_of_order_packets_buffer = []
is_out_of_order = False

track_packet_num_buffer = []    # an array to keep track of packet received number
track_packet_num_time_buffer = []   # an array to keep track of packet received time

last_ack_sent = -1 # calculate the last ack sent based on the packet number and sequence number limit

# if packet_num >= limit
if packet_num > limit:
    last_ack_sent = packet_num % limit - 1
else:
    last_ack_sent = packet_num - 1

all_packets_received = False
track_packet_sent_times_buffer = []    # an array to keep track of each packet sent
track_packet_sent_buffer = []   # an array to keep track of the number of each packets sent
buffer =[]  # a helper array
packets_resent_times = []    # an array to sum up how many times each packet sent for every countdown cycle

# initialize packets_resent_times
for i in range(0,10):
    packets_resent_times.append(0)

# shrink window size to half if packet is dropped
def ShrinkWindowSize(): 
    global win_size, win_size_buffer, win_size_time_buffer
    win_size_time_buffer.append(round(time.time() - start_time, 1))
    if win_size > 1:
        win_size = int(win_size / 2)
        print("Adjust window size from " + str(int(2 * win_size)) + " to " + str(win_size))
    else:
        print("Window size remains to be 4")
    win_size_buffer.append(win_size)

# expand window size twice if no packet is dropped
def ExpandWindowSize():
    global win_size, win_size_buffer, win_size_time_buffer
    win_size_time_buffer.append(round(time.time() - start_time, 1))
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
    # check if expected_packet is 0 or not, if it is 0, then the last packet received is previous cycle limit - 1
    if expected_packet > 0:
        last_packet = expected_packet - 1
    else:
        last_packet = limit - 1
    last_received_packet.append(last_packet)

    if expected_packet < limit:
        expected_packet += 1
    else:
        expected_packet = 0

# calculate good_put every 1000 packets received
def CalculateGoodPut():
    global receive_packets_buffer, good_put_time_buffer, receive_packets, good_put, sent_packets_buffer, sent_packets
    good_put_time_buffer.append(round(time.time() - start_time, 1))
    good_put.append(len(receive_packets_buffer)/sent_packets)
    sent_packets_buffer.append(sent_packets)
    receive_packets_buffer = []
    sent_packets = 0

# calculate avg good put
def CalculateAvgGoodPut():
    global good_put, avg_good_put  
    sum = 0
    for i in range(len(good_put)):
        sum = good_put[i] + sum
    #avg_good_put = sum / len(good_put)
    return round(sum / len(good_put), 2)

# calculate total number of sent packets
def CalculateSentPackets():
    global sent_packets, sent_packets_buffer
    sent_packets = 0
    for i in range(len(sent_packets_buffer)):
        sent_packets = sent_packets_buffer[i] + sent_packets
    return sent_packets

# keep track of the number and the time of packets received 
def TrackReceivedPackets():
    global receive_packets,receive_packets_buffer,track_packet_num_buffer,track_packet_num_time_buffer
    receive_packets += 1
    receive_packets_buffer.append(recent_packet)
    track_packet_num_buffer.append(recent_packet)
    track_packet_num_time_buffer.append(round(time.time()-start_time,1))

# keep track of how many times of each packets to be sent every countdown cycle
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

    for i in range(0,10):
        buffer.append(track_packet_sent_times_buffer.count(i))

    for i in range(0,10):
        packets_resent_times[i] = packets_resent_times[i] + buffer[i]

    track_packet_sent_buffer = []

# start the timer
start_time = time.time()
win_size_time_buffer.append(0)
win_size_buffer.append(win_size)
print("countdown: ", countdown)

while countdown > 0 and all_packets_received == False:

    counter = 0
    last_received_packet = []

    while counter < win_size and all_packets_received == False:

        # get the packets from client
        recent_packet = conn.recv(1024).decode()

        recent_packet = int(recent_packet)
 
        if recent_packet >= limit:
            recent_packet = recent_packet % limit

        sent_packets += 1
        track_packet_sent_buffer.append(recent_packet)

        # if random.random() > 0.01, increment receive_packets, append the packet into receive_packets_buffer and tracket_packet_num_buffer
        if random.random() >= 0.01:

            if countdown == 1 and recent_packet == last_ack_sent:
                if is_packet_lost == False:
                    print("Received the last packet", recent_packet, "\nAll the packets have been received")
                    all_packets_received = True
                else:
                    print("Received packet ", recent_packet, " Expected packet ", expected_packet)
                    is_last_packet_received = True
                TrackReceivedPackets()
                break

            else:
                TrackReceivedPackets()  
                
            # calculate good_put every 1000 packets received
            if len(receive_packets_buffer) == 1000:
                CalculateGoodPut()

            # check if received packet is expected
            if recent_packet == expected_packet:
                print("Received packet ", recent_packet, " Expected packet ", expected_packet)

                # check if received packet reaches limit and set the next expected_packet properly
                if recent_packet == limit - 1:
                    sent_complete = True
                    expected_packet = 0
                    break
                else:
                    sent_complete = False
                    expected_packet += 1

            else:
                print ("Received packet ", recent_packet, " Expected packet ", expected_packet, "Out of order packet", recent_packet )
                out_of_order_packets_buffer.append(recent_packet)
                HandleLostPacket()
                break
        
        # if the packet is lost, append the lost packet to lost_packets_buffer and keep track of the time
        else:
            print ("Lost packet", recent_packet )
            lost_packets_buffer.append(recent_packet)
            lost_packets_time_buffer.append(round(time.time()-start_time,1))

            # if the lost packet reaches limit, then set ack to be previous recent_packet number and break the loop
            if recent_packet == limit - 1: # since packet num starts from 1, the last packet num will be limit - 1
                HandleLostPacket()
                break

            # if the lost packet is the first packet, set is_first_packet_lost to be true
            elif recent_packet == 0:
                HandleLostPacket()
                is_first_packet_lost = True
                break
            else:
                HandleLostPacket()

        counter += 1

    # if all the packets are received, send the last ack to client and break the loop
    if all_packets_received:
        TrackSentPackets()
        print("Sending last Ack ", last_ack_sent)
        print ('*******************************************')
        ack = str(last_ack_sent)
        conn.send(ack.encode()) 
        break

    # handle if last packet is received but there is packet lost
    elif is_last_packet_received:
        ack = last_received_packet[0]
        expected_packet = last_received_packet[0]+1
        is_packet_lost = False
        is_last_packet_received = False

    # if there are packets dropped, send the last received packet cumulative ack and shrink window size
    # handle if the first packet lost in the first countdown cycle
    elif is_first_packet_lost and countdown == int(packet_num / limit) + 1:
        ack = -1
        is_first_packet_lost = False
        is_packet_lost = False
        ShrinkWindowSize()

    # handle if the first packet lost in other countdown cycle
    elif is_first_packet_lost and countdown != int(packet_num / limit) + 1:
        if last_received_packet:
            ack = last_received_packet[0]
        else:
            ack = limit - 1
        is_first_packet_lost = False
        is_packet_lost = False
        ShrinkWindowSize()

    # handle the other packets lost 
    elif is_packet_lost:
        ack = last_received_packet[0]
        expected_packet = last_received_packet[0]+1
        last_received_packet = []
        is_packet_lost = False
        ShrinkWindowSize()

    # if the packet reaches the limit, send the ack of the limit/recent_packet, track sent packets, expand window size
    elif sent_complete:
        ack = recent_packet
        TrackSentPackets()
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

# close the connection
conn.close()

print("Elapsed time: ", round((end_time - start_time)/60, 1))
print("Total packets required:", packet_num)
print("Sent total packets:", CalculateSentPackets())
print("Received total packets:", receive_packets)
print("Lost total packets:", len(lost_packets_buffer))
print("Resent total packets: ",CalculateSentPackets() - packet_num)
print("Average good-put: ", CalculateAvgGoodPut())
# print("Good-put: ", good_put)
# print("Good-put time interval: ", good_put_time_buffer)
# print("Window size: ", win_size_buffer)
# print("Window size time interval: ", win_size_time_buffer)
# print("Lost packets:", lost_packets_buffer)
# print("Lost packets time interval:", lost_packets_time_buffer)
# print("Track received packets num:", track_packet_num_buffer)
# print("Track received packets num time:", track_packet_num_time_buffer)
print("Packet resent time 1:", packets_resent_times[2])
print("Packet resent time 2:", packets_resent_times[3]*2)
print("Packet resent time 3:", packets_resent_times[4]*3)
print("Packet resent time 4:", packets_resent_times[5]*4)
print("Packet resent time 5:", packets_resent_times[6]*5)
print("Packet resent time 6:", packets_resent_times[7]*6)
print("Packet resent time 7:", packets_resent_times[8]*7)
print("Packet resent time 8:", packets_resent_times[9]*8)
print("Resent total packets:",packets_resent_times[2]+packets_resent_times[3]*2+packets_resent_times[4]*3+packets_resent_times[5]*4+packets_resent_times[6]*5+packets_resent_times[7]*6+packets_resent_times[8]*7+packets_resent_times[9]*8)
  
# plot TCP receiver window size over time in the x-axis
plt.figure(figsize=(8,6))
plt.plot(win_size_time_buffer, win_size_buffer)  
# x-axis label
plt.xlabel('Time in seconds')
# y-axis label
plt.ylabel('Window size')
# plot title
plt.title('Window size over time')

# plot TCP sequence number received over time in the x-axis
plt.figure(figsize=(8,6))
plt.plot(track_packet_num_time_buffer,track_packet_num_buffer)
plt.xlabel('Time in seconds')
plt.ylabel('TCP sequence number')
plt.title('TCP sequence number received over time')

# plot TCP sequence number dropped over time in the x-axis
plt.figure(figsize=(8,6))
plt.plot(lost_packets_time_buffer, lost_packets_buffer)  
plt.xlabel('Time in seconds')
plt.ylabel('TCP sequence number')
plt.title('TCP sequence number dropped over time')

# plot TCP sequence number dropped over time in the x-axis
plt.figure(figsize=(8,6))
plt.scatter(lost_packets_time_buffer, lost_packets_buffer, marker='*')
plt.xlabel('Time in seconds')
plt.ylabel('TCP sequence number')
plt.title('TCP sequence number dropped over time')

# plt.figure(figsize=(8,6))
# plt.plot(gootput_time, goodput)
# plt.xlabel('Time in seconds')
# plt.ylabel('Good-put')
# plt.title('Good-put over time')

# function to show the plot
plt.show()

