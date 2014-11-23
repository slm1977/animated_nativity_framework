'''
Created on 26/ott/2014

@author: smonni
'''
# Echo client program
import socket

HOST = 'localhost'        # The remote host
PORT = 50000              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('SNOW_ON')
data = s.recv(1024)
s.close()
print 'Received', repr(data)