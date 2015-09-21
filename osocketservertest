import osocket, threading, time

class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    
    def run(self):
        print(self.socket.readmessage())
        self.socket.close()

s = osocket.OSocket()
host = '127.0.0.1'
port = 16161

s.bind((host, port))

threads = []
while True:
    s.listen(5)
    c, addr = s.accept()
    cc = osocket.OSocket()
    cc.socket = c
    newthread = ClientThread(addr[0], port, cc)
    newthread.start()
    threads.append(newthread)
    
    
