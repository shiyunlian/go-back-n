import socket
hostName = 'https://sjsu.edu/'
try:
    ipAddress = socket.gethostbyname(hostName)
    print(ipAddress)
except:
    print('Unable to get the IP of the host')

# hostName1 = 'www.google.com'
# ipAddress1 = socket.gethostbyname(hostName1)
# print(ipAddress1)

# hostName2 = 'https://sjsu.edu/'
# try:
#     ipAddress2 = socket.gethostbyname(hostName2)
#     print(ipAddress2)
# except:
#     print('Unable to get the IP of the host')
