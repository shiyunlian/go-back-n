import socket, random, time
import matplotlib.pyplot as plt
import threading
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
packet_num = 1000

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
lock = threading.Lock()
ack_buffer=[]
packet_lost = -1

data = conn.recv(1024).decode()
print(data)
a_list = data.split('.')
print(a_list)
print(len(a_list))
a_list= [int(i) for i in a_list]
print(a_list)
print(len(a_list))


# while all_packets_received == False:
#     ack_buffer=[]
#     counter = 0
#     count = 0
#     range = win_size
#     while counter < range and all_packets_received == False:
#     # while all_packets_received == False:
#         # lock.acquire()
#         recent_packet = conn.recv(1024).decode()

#         recent_packet = int(recent_packet)
#         print("Sent packet",recent_packet)
#         # lock.release()

#         if recent_packet >= limit:
#             recent_packet = recent_packet % limit

#         sent_packets += 1
#         track_packet_sent_buffer.append(recent_packet)

#         if random.random() >= 0.01:

#             # if recent_packet == expected_packet:
#             print("received packet", recent_packet)
#             if not is_packet_lost:
#                 ack_buffer.append(recent_packet)
#                 ExpandWindowSize()

#             # if there are packets lost previousy
#             else:
#                 ack_buffer.append(last_received_packet[0])

#                 # print("sent ack", ack)
#                 # print("****************")
#                 expected_packet = expected_packet + 1
#                 # ExpandWindowSize()
#                 # lock.release()
            
#             # else:
#             #     ack = str(last_received_packet[0])
#             #     conn.send(ack.encode())
#                 # ShrinkWindowSize()
#                 # lock.release()

#         else:
#             print ("Lost packet", recent_packet )
#             lost_packets_buffer.append(recent_packet)
#             lost_packets_time_buffer.append(round(time.time()-start_time,1))
#             is_packet_lost = True

#             # check if expected_packet is 0 or not, if it is 0, then the last packet received is previous cycle limit - 1
#             if recent_packet == limit - 1:
#                 HandleLostPacket()
#                 break
#             elif recent_packet == 0:
#                 HandleLostPacket()
#                 is_first_packet_lost = True
#                 break
#             else:
#                 HandleLostPacket()

#             if expected_packet < limit:
#                 expected_packet += 1
#             else:
#                 expected_packet = 0
            
#             if count == 0:
#                 ShrinkWindowSize()
#             count += 1
#             ack_buffer.append(packet_lost)
#             # lock.release()

#         counter += 1

#     i = 0
#     while i < len(ack_buffer):
#         conn.send(str(ack_buffer[i]).encode())
#         time.sleep(0.05)
#         i += 1


    # for i in range(len):
    #     conn.send(str(ack_buffer[i]).encode())
    #     time.sleep(0.05)
    

