import socket, time
from timer import Timer
import threading
import asyncio

import statistics
from statistics import mode
#serverName='172.16.210.4'
serverName='10.0.0.175'
#serverName='127.0.0.1'
#serverName = '10.0.0.81'

host = socket.gethostname() 
ip =  socket.gethostbyname(host)
port = 12340 # socket server port number
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
print(ip)
# initiates the TCP connection between the client and server.
client_socket.connect((host, port)) 
#client_socket.connect((serverName, port)) 
# send an initial message through the client’s socket and into the TCP connection
request = 'network'
client_socket.send(request.encode())

# receive response from server
response = client_socket.recv(1024).decode()
print('From Server:' , response)


win_size = 128
win_size_buffer = []
win_size_time_buffer = []

limit = 65536
packet_num = 1000
ack = -1
countdown = int(packet_num / limit)+1
print("Total number of packets to be sent is ", packet_num)

last_ack_sent = -1 # calculate the last ack sent based on the packet number and sequence number limit
if packet_num > limit:
    last_ack_sent = packet_num % limit - 1
else:
    last_ack_sent = packet_num - 1

send_base = 0
next_seqnum = 0
ack_buffer = []
seqnum_buffer = []
seqnum_time_buffer =[]
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

def StartTimer():
    start=time.time
    
# start the time
start_time = time.time()
expected_ack = 0
lock = threading.Lock()
ack_buffer = []
packet_buffer=[]
is_packet_lost = False

packet_list=''
while next_seqnum < send_base + win_size:
    packet_list = packet_list+str(next_seqnum)+'.'
    # if next_seqnum == send_base + win_size - 1:
    #     packet_list = packet_list+str(next_seqnum)
    # else:
    #     packet_list = packet_list+str(next_seqnum)+'.'
    next_seqnum += 1
    
packet_list = packet_list[:-1]
client_socket.send(packet_list.encode())
print(packet_list)
# while countdown > 0:
#     counter = 0
#     recent_ack = -1
#     # send all the packets in the window
#     # while next_seqnum < send_base + win_size:
#     #     packet_buffer.append(next_seqnum)
#     #     next_seqnum += 1
    
#     # for i in range(len(packet_buffer)):
#     #     client_socket.send(str(packet_buffer[i]).encode())
#     count = 0
    
#     if is_packet_lost:
#         next_seqnum = int(mode(ack_buffer) + 1)
#         print(mode(ack_buffer))
#         print(ack_buffer)
#         is_packet_lost = False
#         print("next seqnum", next_seqnum)

#     ack_buffer=[]

#     # while seq_num <= packet_num:
# #     if seq_num < limit:
# #         packet_list = packet_list+str(seq_num)
# #     else:
# #         packet_list = packet_list+str(seq_num % limit)
# #     seq_num += 1

#     while next_seqnum < send_base + win_size:
#         packet_list = packet_list+str(next_seqnum)+'.'
#         #next_seqnum = str(next_seqnum)
#         # client_socket.send((str(next_seqnum)+'/').encode())
#         # print("send packet", next_seqnum)
#         #time.sleep(0.05)
#         next_seqnum += 1
    

#     client_socket.send(packet_list.encode())
#     # range = win_size
    
#     # counter = 0
#     # while counter < range:
#     #     ack = client_socket.recv(1024).decode()
#     #     ack = int(ack)
#     #     ack_buffer.append(ack)
#     #     if ack == send_base:
#     #         print("ack",ack)
#     #         send_base = send_base + 1
#     #         ExpandWindowSize()
#     #     elif ack == send_base - 1:
#     #         print("ack",ack)
#     #         if count == 0:
#     #             ShrinkWindowSize()
#     #             count += 1
#     #     else:
#     #         is_packet_lost = True    
#     #     counter += 1
    
    
        

#     # print(ack_buffer)
#     # ack_buffer.append(ack)
#     # print(ack_buffer)
#     # t = Timer()
#     # ack_range = win_size
#     # time.sleep(0.01)
#     # while counter < ack_range:
#     #     time.sleep(0.01)
#     #     ack = client_socket.recv(1024).decode()
#     #     ack_buffer.append(ack)
#     #     print(ack_buffer)
#         # ack = int(ack)
#         # if ack == expected_ack:
#         #     send_base = send_base + 1
#         #     print("received ack", ack)
#         #     recent_ack = expected_ack
#         #     expected_ack = expected_ack + 1
#         #     # ExpandWindowSize()
#         # else:
#         #     # t.start()
#         #     print("not received ack", ack)
        

    

#     # t = Timer()
#     # ack_range = win_size
#     # while counter < ack_range:
#     #     lock.acquire()
#     #     ack = client_socket.recv(1024).decode()
#     #     if ack == expected_ack:
#     #         send_base = send_base + 1
#     #         print("received ack", ack)
#     #         recent_ack = expected_ack
#     #         expected_ack = expected_ack + 1
#     #         # ExpandWindowSize()
#     #     else:
#     #         t.start()
#     #         print("not received ack", ack)
#     #     lock.release()
#     #     counter = counter + 1

#         # 0123
#         # if ack is expected, increment send_base, expected_ack
        
            
#             # if send_base == next_seqnum:
#             #     t.stop()
#             # else:
#             #     t.start()

        
        
#         # else:
#         #     ShrinkWindowSize()

#         # if t.timeout():
#         #     t.start()
#         #     while send_base != next_seqnum - 1:
#         #         send_base = str(send_base)
#         #         client_socket.send(send_base.encode())
#         #         send_base = int(send_base) + 1


#         # # if ack is the last ack to be received, all the packets have sent successfully
#         # if countdown == 1 and ack == last_ack_sent:
#         #     countdown -= 1
#         #     print("All the packets have sent.")
#         #     break
        
#         # # if the first packet is lost in the first countdown, send_base is 0
#         # elif ack == -1:
#         #     send_base = 0

#         # # check if the ack reaches limit, set the send_base appropriately, and expand window size
#         # elif ack == limit - 1:
#         #     countdown -= 1 
#         #     send_base = 0
#         #     print("Countdown", countdown)
#         # else:
#         #     send_base = ack + 1
#         #     print ('Received ACK', ack, "Expected Ack",expected_ack) 

#         # # if all the packets sent are acknowledged, expand the window, otherwise, shrink the window
#         # if ack == int(expected_ack):
#         #     ExpandWindowSize()
#         # else:
#         #     ShrinkWindowSize()
    



    