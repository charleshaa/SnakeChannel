import socket

class Client:

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(("127.0.0.1", port))
        self.seqNum = 0

    def send_message(self, message):
        self.sock.send(message)
        print "Client " + self.name + " sent message ", message

    def leave(self):
        self.sock.close()
        print "Client " + self.name + " left the game"
