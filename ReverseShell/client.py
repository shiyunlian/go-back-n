import socket
import sys

# create a socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global s

        host=''
        port=9999
        s=socket.socket()
    except socket.error as msg:
        print("socket creation error:" + str(msg))
        
# bind the socket and listen for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("binding the port" + str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        pritn("socket binding error:" + str(msg) +'\n' + "retrying...")
        bind_socket()

# establish connection with a client (socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("connection has been established" + "IP" + address[0] + "|Port" + str(address[1]))
    send_
    conn.close()


