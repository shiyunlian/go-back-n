import sys
import time
import random
import signal
import threading
import socket
from struct import *

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

seqNum = 0
firstInWindow = -1
lastInWindow = -1
lastAcked = -1
numAcked = -1

sendComplete = False
ackedComplete = False

sendBuffer = []
timeoutTimers = []
windowSize = 4
TIMEOUT=0.5
lock = threading.Lock()

## Resend packets in the window
def ResendPackets():
	global sendBuffer
	global client_socket
	global TIMEOUT
	global timeoutTimers
	global lastInWindow
	global firstInWindow
	global host
	global port
	global windowSize

	iterator = firstInWindow
	while iterator <= lastInWindow:
		if sendBuffer[iterator % windowSize] != None:
			packet = sendBuffer[iterator % windowSize]
			print ("Resending packet: S" + str(iterator) + "; Timer started")
			client_socket.send(packet.encode())
			timeoutTimers[iterator % windowSize] = TIMEOUT
		iterator += 1

## Keep track of the timeout values which are sent to the server
def Signalhandler(signum, _):
	global firstInWindow
	global lastInWindow
	global sendBuffer
	global lock
	global timeoutTimers
	global windowSize


	for i, eachtimer in enumerate(timeoutTimers):
		timeoutTimers[i] = eachtimer - 1
    
	if len(timeoutTimers) > (firstInWindow % windowSize) and timeoutTimers[firstInWindow % windowSize] == 0:
		print ("Timeout, sequence number =", firstInWindow)
		lock.acquire()
		ResendPackets()
		lock.release()


## Look for acknowledgements from the server
def LookforACKs():
	global firstInWindow
	global sendBuffer
	global windowSize
	global client_socket
	global numAcked
	global seqNum
	global ackedComplete
	global sendComplete
	global lastAcked
	global lastInWindow

	# Protocol = Go back N

	while not ackedComplete:
		packet=client_socket.recv(1024).decode()
        ack = unpack('IHH', packet)
        ackNum = ack[0]
		
        if ackNum == seqNum:
            print ("Received ACK: ", ackNum)
            lock.acquire()
            iterator = firstInWindow
            while iterator <= lastInWindow:
                sendBuffer[iterator % windowSize] = None
                timeoutTimers[iterator % windowSize] = 0
                lastAcked = lastAcked + 1
                firstInWindow = firstInWindow + 1
            lock.release()
        elif ackNum == lastAcked + 1:
            print ("Received ACK: ", ackNum)
            lock.acquire()
            sendBuffer[ackNum % windowSize] = None
            timeoutTimers[ackNum % windowSize] = 0
            lastAcked = lastAcked + 1
            firstInWindow = firstInWindow + 1
            lock.release()

        # If all packets sent and all acknowledgements received
        if sendComplete and lastAcked >= lastInWindow:
            ackedComplete = True
        else:
            print ("Ack " + str(ackNum) + " lost (Info for simulation).")



# Start thread looking for acknowledgements
threadForAck = threading.Thread(target=LookforACKs, args=())
threadForAck.start()

signal.signal(signal.SIGALRM, Signalhandler)
signal.setitimer(signal.ITIMER_REAL, 0.01, 0.01)

firstInWindow = 0

# Send packets
while not sendComplete:
	toSend = lastInWindow + 1
	data = GetMessage()
	header = int('0101010101010101', 2)
	cs = pack('IH' + str(len(data)) + 's', seqNum, header, data)
	checksum = CalculateChecksum(cs)

	packet = pack('IHH' + str(len(data)) + 's', seqNum, checksum, header, data)
	if toSend < windowSize:
		sendBuffer.append(packet)
		timeoutTimers.append(TIMEOUT)
	else:
		sendBuffer[toSend % windowSize] = packet
		timeoutTimers[toSend % windowSize] = TIMEOUT

	print "Sending S" + str(seqNum) + "; Timer started"
	if BIT_ERROR_PROBABILITY > random.random():
		error_data = "0123456789012345678012345678012345678012345678012345678"
		packet = pack('IHH' + str(len(error_data)) + 's', seqNum, checksum, header, data)
	clientSocket.sendto(packet, (host, port))

	lastInWindow = lastInWindow + 1
	seqNum = seqNum + 1

while not ackedComplete:
	pass
	
	