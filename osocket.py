import socket

class OSocketException(Exception):
    pass

class OSocketSendMustBeBytes(Exception):
    pass

class OSocket:
    def __init__(self, timeout=60):
        self.socket = socket.socket()
        self.socket.settimeout(timeout)
        self.buffer = b''
        
    def connect(self, host, port):
        self.socket.connect((host, port))

    def settimeout(self, timeout):
        self.socket.settimeout(timeout)

    def readmessage(self):
        ret = self.buffer
        lengthFound = False
        length = 0
        lastLengthByte = 0
        lastMask = 1
        
        while (True):
            
            while (not lengthFound and len(ret) > lastLengthByte):
                curlbyte = ret[lastLengthByte]
                if (curlbyte >= 128):
                    length += lastMask * (curlbyte % 128)
                    lastMask *= 128
                    lastLengthByte += 1
                else:
                    length += lastMask * (curlbyte % 128)
                    lastLengthByte += 1
                    lengthFound = True
            if (lengthFound):
                if (len(ret) - lastLengthByte == length):
                    self.buffer = ret[length:]
                    return ret[lastLengthByte:length+1]
            
            rawbytes = self.socket.recv(512)
            if (rawbytes == b''):
                raise (OSocketException)
            
            ret += rawbytes
    
    def sendmessage(self, message):
        
        if (type(message) != bytes):
            raise (OSocketSendMustBeBytes)

        k = len(message)

        l = []

        while (k > 0):
            t = k % 128
            k = k // 128
            if (k > 0):
                t += 128

            l.append(t)

        self.socket.send(bytes(l) + message)

        

    def bind(self, a):
        return self.socket.bind(a)
    
    def listen(self, num):
        return self.socket.listen(num)

    def accept(self):
        return self.socket.accept()

    def close(self):
        return self.socket.close()
