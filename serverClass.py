import socket
import time
import select
from random import randint

class Server:

	def __init__(self, port):
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("127.0.0.1", self.port))
		self.seqNum = 0
		self.DATASIZE = 1024
		self.listening = False
		self.clients = []
		self.Pnum = 19

	def stop_listening(self):
		if(self.listening == False):
			return True
		self.listening = False
		print "Server stopped listening on port ", self.port

	def clientsIndex(self, addr): #Retourne l'index du client dans clients[] en fonction de son tuple addresse (-1 si non trouve)
		for index, ClientData in enumerate(self.clients):
			if ClientData.addr == addr:
				return index
		return -1

	def listen(self):
		if(self.listening == False):
			self.listening = True
		while self.listening:
			readable, writable, exceptional = select.select([self.sock], [], [self.sock])#Attent la reception d'un message
			for s in readable: #Pour chaque socket qui dispose d'un message a lire...
				data, addr = self.sock.recvfrom(self.port) #On recupere les data
				print data
				data = data.split(" ") #On split les data
				if Server.clientsIndex(self, addr) == -1: #Si l'addr n'est pas connu
					if data[0] == "GetToken" and data[2] == "Snake":#On verifie la logique protocolaire
						self.clients.append(ClientData(addr, data[1]))#On cree un client pour l'address de l'expeditaire
					else:
						continue#Si le client n'est pas connu et qu'il ne rescpect pas le protocol, on retourne a l'ecoute de packet.
				client = self.clients[Server.clientsIndex(self, addr)]#On sort le client correspondant a l'addr expediteur
				for case in switch(client.etat):#Pour tout les etat possible du client...
					if case("conn_request"):#Si etat conn_request
						client.tokenB = randint(0, 0xFFFFFFFF)#On genere un token B
						self.sock.sendto("Token " + str(client.tokenB)+" "+str(client.tokenA)+" "+str(self.Pnum), addr)#On envoi ce token
						client.etat = "conn_accept"#On met a jour l'etat du client afin d'avancer dans la logique protocolaire
						break
					if case("conn_accept"):#Si etat conn_accept
						if data[0] == "Connect":
							data = data[1].split("\\", 4)#Formate les data
							del data[0]#idem
							if data[1] == str(client.tokenB) and data[3] == str(self.Pnum):#Si la reponse correspond a la logique protocolaire...
								self.sock.sendto("Connected " + str(client.tokenB), addr)#Envoi la confirmation de connection au client
								client.etat = "connected"#Passe l'etat du client a connecte
								client.compteur = 0
						else:
							if client.compteur >2:
								client.etat = "conn_request"#Si le message n'est pas ce qu'on attend, le client regresse dans la machine d'etat
							else:
								client.compteur += 1
						break
					if case("connected"):
						if data[0] == "Connect" or "GetToken":
							if client.compteur > 2:
								client.etat = "conn_accept"
							else:
								client.compteur += 1
						else:
							print "message from connected client :", data
						break


class ClientData: #Contient les donnes pour chaque client
	def __init__(self, addr, token):
		self.addr = addr
		self.etat = "conn_request"
		self.tokenA = token
		self.compteur = 0

#This switch class comes from http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False