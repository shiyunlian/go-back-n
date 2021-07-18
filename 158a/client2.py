import time, socket

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
ack_buffer =[]
win_size = 4
win_size_buffer = []
win_start = 0
win_end = 0
data = -1
limit = 100
packet_num = 1500
countdown = int(packet_num / limit)
print("Total number of packets to be sent is ", packet_num)
counter = 0
seq_num = 0
expected_packet = 0
packet_list = ""
flag = 0
ack = -1
sent_complete = False
last_received_packet = []
# receive_ack_buffer=[]
# while seq_num <= packet_num:
#     if seq_num < limit:
#         packet_list = packet_list+str(seq_num)
#     else:
#         packet_list = packet_list+str(seq_num % limit)
#     seq_num += 1

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

recent_packet = 0

# start the time
start_time = time.time()

while countdown > 0:

    counter = 0

    # send the packets
    while counter < win_size:
        if win_start + counter >= limit:
            break
            # recent_packet = str((win_start + counter) % limit)
        else:
            recent_packet = str(win_start + counter)

        client_socket.send(recent_packet.encode())
        print("Sent packet", recent_packet)
        counter += 1
        time.sleep(0.2)

    time.sleep(0.5)

    # receive ack from server
    ack = client_socket.recv(1024).decode()

    if not ack:
        break

    ack = int(ack)
    if ack == -1:
        win_start = 0

    # check if the ack reaches limit, set the win_start appropriately
    if ack == limit - 1:
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
    
    win_end = win_start + win_size - 1

# end time and calculate elapsed_time
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time: ", elapsed_time)
# close the connection
client_socket.close()