from socket import *
# serverName = ’servername’
# serverName='172.16.210.4'
# serverName='10.0.0.175'
serverName='127.0.0.1'
serverPort = 12000

# creates the client’s socket,the first parameter indicates the underlying network is using IPv4. 
# The second parameter indicates that the socket is a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiates the TCP connection between the client and server.
clientSocket.connect((serverName,serverPort))

#obtains a sentence from the user.
sentence = input('Input lowercase sentence:')

#sends the sentence through the client’s socket and into the TCP connection.
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)

print('From Server:' , modifiedSentence.decode())

#closes the socket and closes the TCP connection
clientSocket.close()