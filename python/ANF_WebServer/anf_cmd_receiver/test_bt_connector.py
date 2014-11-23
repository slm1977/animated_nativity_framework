'''
Created on 01/nov/2014

@author: smonni
'''
import sys
from bluetooth import *

#HOST = sys.argv[1]       # The remote host
#PORT = 8888                 # Server port

# arduno MAC ADDRESS
MAC_ADDR="20:14:08:05:06:84"
s=BluetoothSocket( RFCOMM )

#s.connect((HOST, PORT))
s.connect((MAC_ADDR, 1))
while True :
   message = raw_input('Send:')
   if not message : break
   s.send(message)
   data = s.recv(1024)
   print 'Received', `data`
   
print "No Message"
print "Closing connection"
s.close()