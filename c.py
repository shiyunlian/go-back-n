import time, socket, random

s = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")")
host = '10.0.0.175'
port = 1234
print("Trying to connect to " + host)
s.connect((host, port))
print("Connection established.")

while True:

    message=s.recv(1024).decode()
    if(message=='exit'):
        print("Program terminated.")
        break
    seq_num_range=pow(2,int(message))-1
    win_begin=0
    ack_message=""
    message=""
    while win_begin!=seq_num_range:
           
       random_num=random.randint(0,9)
       if(random_num==0):
          ack_message="ACK Lost"
          message = s.recv(1024).decode()
          s.send(ack_message.encode())

       else:
          ack_message="ACK "+str(win_begin)
          message = s.recv(1024).decode()
          s.send(ack_message.encode())
          win_begin=win_begin+1
   