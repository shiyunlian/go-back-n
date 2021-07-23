from timer import Timer
import socket
t = Timer()

t.start()
host = socket.gethostname() 
ip =  socket.gethostbyname(host)
port = 12340  # socket server port number
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
t.stop()