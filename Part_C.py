import socket
PORT = 12341
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',PORT))

connection_num = 10
count = 1
# try to establish connection and send response back to client
while connection_num > 0:

    try:
        serverSocket.listen(connection_num)
        print('Server is listening...')
        conn, address = serverSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        response = 'Thank you' 
        conn.send(response.encode())
        print('Sent thank you message', count)
        count += 1
        print('*******************************')
    except:
        print('Server is not listening...')

    connection_num -= 1

# close the connection
conn.close() 
print('Connection closed.') 
