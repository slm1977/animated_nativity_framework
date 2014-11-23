'''
Created on 26/ott/2014

@author: smonni
'''

import socket


import threading
from bluetooth import BluetoothSocket, RFCOMM

class SocketThread (threading.Thread):
    def __init__(self, command,host="localhost", port=50000):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.host = host
        self.port = port
        self.command = command
        self.start()
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(self.command)
        data = s.recv(1024)
        s.close()

class BT_ClientSocketThread (threading.Thread):
    def __init__(self, command,MAC_ADDRESS="20:14:08:05:06:84", port=1):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.command = command
        self.MAC_ADDRESS = MAC_ADDRESS
        self.port = port
        self.bt = BluetoothSocket( RFCOMM )
        self.start()
        
    def run(self):
        self.bt.connect((self.MAC_ADDRESS, self.port))
        self.bt.send(self.command)
        
        response = self.bt.recv(1024)
        print 'Bluetooth Received:'+ response
        self.bt.close()
        
        
class ClientSocket:
    def __init__(self, command):
        HOST = 'localhost'        # The remote host
        PORT = 50000              # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(command)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)