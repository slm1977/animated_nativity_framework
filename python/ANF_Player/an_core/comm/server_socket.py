'''
Created on 26/ott/2014

@author: smonni
'''
import  socket
 



import threading
class SocketThread (threading.Thread):
    def __init__(self, cmd_received_cb, host="", port=50000):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.host = host
        self.port = port
        self.exit_flag=False
        self.cmd_received_cb = cmd_received_cb
        
    def run(self):
        # http://www.python.it/doc/howto/Socket/sockets-it/sockets-it.html
        # crea un socket INET di tipo STREAM
        
       
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        
        # associa il socket a un host pubblico
        # e a una delle porte ben-note
        #serversocket.bind((socket.gethostname(), 80))
        print "Server socket on port: %s" % self.port
        # associa solo in locale per performance....
        serversocket.bind((self.host, self.port))
        # diventa un socket server
        serversocket.listen(5)

        print "Starting " + self.name
        while not self.exit_flag:
            conn, addr = serversocket.accept()
            print 'Connected by', addr
            data = conn.recv(1024)
            if not data: 
                print "No data received. Closing connection"
                conn.close() 
            else:
                self.cmd_received_cb(data)
                conn.send("Ok")
 


class TestSocketThread:
    def __init__(self):
        st = SocketThread(self.on_data_received)
        st.start()
        
    def on_data_received(self, data):
        print "Data received from the client:%s" % data
        
        
if __name__ == "__main__":
    ts = TestSocketThread() 
    while 1:
        pass
    
        
        