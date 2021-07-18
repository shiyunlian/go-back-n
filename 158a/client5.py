import socket, time

# serverName='172.16.210.4'
# serverName='10.0.0.175'
# serverName='127.0.0.1'
#serverName = '10.0.0.81'

host = socket.gethostname() 
port = 12340  # socket server port number
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  

# initiates the TCP connection between the client and server.
client_socket.connect((host, port)) 

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
client_socket.send(request.encode())

# receive response from server
response = client_socket.recv(1024).decode()
print('From Server:' , response)

win_size = 1
win_size_buffer = []
win_size_time_buffer = []
win_start = 0
win_end = win_start + win_size - 1
limit = 65536
packet_num = 10000
recent_packet = 0
ack = -1
countdown = int(packet_num / limit)+1
print("Total number of packets to be sent is ", packet_num)

last_ack_sent = -1 # calculate the last ack sent based on the packet number and sequence number limit
if packet_num > limit:
    last_ack_sent = packet_num % limit - 1
else:
    last_ack_sent = packet_num - 1

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
    global win_size, win_size_buffer
    win_size_time_buffer.append(round(time.time() - start_time, 1))
    if win_size < 128:
        win_size = int(2 * win_size)
        print("Adjust window size from " + str(int(win_size/2)) + " to " + str(win_size))
    else:
        print("Window size remains to be 128")
    win_size_buffer.append(win_size)

# start the time
start_time = time.time()
win_size_time_buffer.append(0)
win_size_buffer.append(win_size)
print("countdown: ", countdown)

while countdown > 0:

    counter = 0

    # send the packets
    while counter < win_size:

        # if the packet num to be sent is the last packet and it is the last countdown
        if win_start + counter == last_ack_sent and countdown == 1:
            recent_packet = str(win_start + counter)
            client_socket.send(recent_packet.encode())
            print("Sent packet", recent_packet)
            break

        # if the packet num to be sent is greater than limit, break the loop
        if win_start + counter >= limit:
            break
            # recent_packet = str((win_start + counter) % limit)
        else:
            recent_packet = str(win_start + counter)

        client_socket.send(recent_packet.encode())
        print("Sent packet", recent_packet)
        counter += 1
        time.sleep(0.01)

    #time.sleep(0.01)

    # receive ack from server
    ack = client_socket.recv(1024).decode()

    ack = int(ack)
    
    # if ack is the last ack to be received, all the packets have sent successfully
    if countdown == 1 and ack == last_ack_sent:
        countdown -= 1
        print("All the packets have sent.")
        break
    
    # if the first packet is lost in the first countdown, reset window start to be 0
    elif ack == -1:
        win_start = 0

    # check if the ack reaches limit, set the window start appropriately, and expand window size
    elif ack == limit - 1:
        countdown -= 1 
        win_start = 0
        print("Countdown", countdown)
    else:
        win_start = ack + 1
    print ('Received ACK', ack) 

    # if all the packets sent are acknowledged, expand the window, otherwise, shrink the window
    if ack == int(recent_packet):
        ExpandWindowSize()
    else:
        ShrinkWindowSize()

# end time and calculate elapsed_time
end_time = time.time()
print("Elapsed time: ", round(end_time - start_time, 1))
# print("Window size: ", win_size_buffer)
# print("Window size time interval: ", win_size_time_buffer)

# close the connection
client_socket.close()