import socket, time, statistics
from statistics import mode

serverName='10.0.0.175'

host = socket.gethostname() 
ip =  socket.gethostbyname(host)
print(host, "ip address: ", ip)

# initiates the TCP connection between the client and server.
port = 12340 # socket server port number 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#client_socket.connect((host, port)) 
client_socket.connect((serverName, port)) 

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
client_socket.send(request.encode())

# receive response from server
response = client_socket.recv(1024).decode()
print('From Server:' , response)

win_size = 1
win_size_buffer = []
win_size_time_buffer = []

# use two pointers to keep track of the window size between [send_base, next_seqnum -1], intial send_base and next_seqnum are 0
send_base = 0
next_seqnum = 0
is_packet_lost = False
is_all_packets_sent = False
limit = 65536
packet_num = 100000
countdown = int(packet_num / limit)+1
print("Total number of packets to be sent is", packet_num, "Countdown is", countdown)

last_ack_sent = -1 # calculate the last ack sent based on the packet number and sequence number limit
if packet_num > limit:
    last_ack_sent = packet_num % limit - 1
else:
    last_ack_sent = packet_num - 1

# shrink window size to half if packet is dropped
def ShrinkWindowSize(): 
    global win_size, win_size_buffer
    if win_size > 1:
        win_size = int(win_size / 2)
        print("Adjust window size from " + str(int(2 * win_size)) + " to " + str(win_size))
    else:
        print("Window size remains to be 4")
    win_size_buffer.append(win_size)

# expand window size twice if no packet is dropped
def ExpandWindowSize():
    global win_size, win_size_buffer
    if win_size < 128:
        win_size = int(2 * win_size)
        print("Adjust window size from " + str(int(win_size/2)) + " to " + str(win_size))
    else:
        print("Window size remains to be 128")
    win_size_buffer.append(win_size)
while countdown > 0:

    packet_list=''
    ack_list=''

    # create a packet list in window size and send to server
    while next_seqnum < send_base + win_size:

        if next_seqnum == last_ack_sent and countdown == 1:
            packet_list = packet_list + str(next_seqnum) + '.'
            break

        # if the packet num to be sent is greater than limit, break the loop
        if next_seqnum >= limit:
            break
        else:
            packet_list = packet_list + str(next_seqnum) + '.'

        print('Send next seq',next_seqnum)
        next_seqnum += 1
    
    # remove the last character '.'
    packet_list = packet_list[:-1]

    # send the packet list to server
    client_socket.send(packet_list.encode())

    # receive the ack list from client
    ack_list = client_socket.recv(1024).decode()

    # if ack list has more than 1 acks, ack list needs to split
    if len(ack_list) > 1 :
        ack_list = ack_list.split('.')

    # convert string acks into integer acks
    ack_list=[int(i) for i in ack_list]

    # check each ack to see if there is packet dropped
    count = 0 # count if there is packet dropped

    for i in range(len(ack_list)):

        # check if all the packets have sent and received successfully
        if countdown == 1 and ack_list[i] == send_base and send_base == last_ack_sent:
            countdown -= 1
            is_all_packets_sent = True
            print('ack', ack_list[i], "\nAll the packets have sent.")
            break

        # packet received and expand window size
        if ack_list[i] == send_base:
            print('ack', ack_list[i])

            # if ack is 65535, send_base will start from 0, countdown decrement by one
            if ack_list[i] == limit - 1:
                send_base = 0
                countdown -= 1

            # if ack is 0~65534, send_base increment by one
            else:
                send_base = send_base + 1
            ExpandWindowSize()

        # packet dropped and shrink window size
        else:
            is_packet_lost = True
            print("ack", ack_list[i])
            if count == 0:
                ShrinkWindowSize()
                count += 1

    if is_all_packets_sent:
        break

    # find the correct next_seqnum if packet dropped
    if is_packet_lost:
        if ack_list[0] == -1:
            next_seqnum = 0
        else:
            next_seqnum = mode(ack_list) + 1
        is_packet_lost = False
    
    if next_seqnum == limit:
        next_seqnum = 0
        send_base = 0
    
    print("next seqnum", next_seqnum)
    
print(host, "ip address: ", ip)

# close the connection
client_socket.close()