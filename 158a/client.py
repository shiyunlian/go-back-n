#Name    : Sayali Deo
#Roll No : 7926
#Class   : TE Computers
#Batch   : A

# Go Back N ARQ. Client Side Code
#Assume sender is sending frames continously.
import socket


def client_program():
	n = 4
	win_start=0
	win_end = 2
	host = socket.gethostname()  # as both code is running on same pc
	port = 1234  # socket server port number

	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
	client_socket.connect((host, port))  # connect to the server
	print ('Window Size is ', n)
	data=""

	while data != "15":
         count=0
		#  print ("Sending frames...")

        while count <= n:
            if win_start + count <= 15:
                print ("Frame -> ", win_start + count)
                count = count+1
            else:
                break
		
		msg = str(win_start)
		client_socket.send(msg.encode())  # send message
		data = client_socket.recv(1024).decode()  # receive NAK
		msg = str(data)
		win_start = int(msg)
		win_end = win_start + n - 1
		print ("************************************")
		print ('Received ACK server: ' + data)  # show in terminal

	client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()



