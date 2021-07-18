import time, socket

# serverName='172.16.210.4'
# serverName='10.0.0.175'
# serverName='127.0.0.1'
#serverName = '10.0.0.81'

host = socket.gethostname() 
port = 1234  # socket server port number
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  

# initiates the TCP connection between the client and server.
client_socket.connect((host, port)) 

# send an initial message through the client’s socket and into the TCP connection
request = 'network'
client_socket.send(request.encode())

# receive response from server
response = client_socket.recv(1024).decode()
print('From Server:' , response)

win_size = 4
win_start = 0
win_end = 0
data = -1
limit = 100
packet_num = 1000 - 1
count = int(packet_num + 1 / limit)
print("Total number of packets to be sent is ", packet_num + 1)

# seq_num = 0
# packet_list = ""
# while seq_num <= packet_num:
#     if seq_num <= limit:
#         packet_list = packet_list+str(seq_num)
#     else:
#         packet_list = packet_list+str(seq_num % limit)
#     seq_num += 1

while data <= packet_num and count > 0:
    msg = str(win_start)
    client_socket.send(msg.encode())

    data = client_socket.recv(1024).decode()
    
    if not data:
        break

    data = int(data)
    # if data <= 65535:
    #     win_start = data + 1
    # else:
    #     win_start = 0
    if data == limit:
        count -= 1 
    if data == -1 and count != int(packet_num + 1 / limit):
        print('Received Ack ' + limit)
    win_start = data + 1
    win_end = win_start + win_size - 1
    print ('Received ACK ', data) 

# close the connection
client_socket.close()