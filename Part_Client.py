import socket

host = socket.gethostname() 
port = 12341  # socket server port number
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
connection_num = 10

# initiates the TCP connection between the client and server.
while connection_num > 0:
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    client_socket.connect((host, port)) 

# receive response from server
    response = client_socket.recv(1024).decode()
    print(response)
    connection_num -= 1

client_socket.close()