import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),5000))
s.listen(5)
while True:
    conn,addr=s.accept()
    print(f"Connection to {addr} established")
    conn.send(bytes("Socket programming","utf-8"))
    conn.close()