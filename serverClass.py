import socket
import time

class Server:

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", self.port))
        self.seqNum = 0
        self.DATASIZE = 1024
        self.listening = False
        self.clients = []

    def add_client(self, client):
        self.clients.push(client)
        for c in clients
            print c[0]


    def listen(self):
        if(self.listening == False):
            self.listening = True
        time.sleep(1);
        while self.listening:
            print "Server listening on 127.0.0.1:" + str(self.port)
            data, addr = self.sock.recvfrom(self.DATASIZE)
            print "received :", data

    def stop_listening(self):
        if(self.listening == False):
            return True
        self.listening = False
        print "Server stopped listening on port ", self.port
