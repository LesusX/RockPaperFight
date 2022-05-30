import socket
import pickle
'''
The Network file is responsible for the comunication between the clients and the server. 
'''
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "SET_IPv4_HERE" 
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()
    # Get players id 
    def getP(self):
        return self.p
    # Connect to server 
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096*6).decode()
        except:
            pass
    # Sent/recieve all data in string form
    # TODO: In the future let objects be sent and recieved as well.  
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*6))
        except socket.error as e:
            print(e) 
