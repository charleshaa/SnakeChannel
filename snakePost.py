import socket
import Queue
import random
import pygame
from pygame.locals import *
from Color import color
from struct import *
from snakeChan import SnakeChan

#commDict = {addr, ListDeData}
#ackDict = {addr, ListDeAck}

class SnakePost:

	def __init__(self, canalTransmission):
		pygame.init()
		pygame.time.set_timer(USEREVENT+1, 30)
		self.canalTransmission = canalTransmission
		self.commDict = {}
		self.ackDict = {}
		print color.GREEN + "snakePost instanciated." + color.END

	def send(self, data, addr, seq=0, ack=0):
		AckToSendToAddr = self.ackDict.get(addr) #Recupere la liste des ack a faire pour cette addresse
		if AckToSendToAddr: #Si il y au moins un ack a faire
			ack = AckToSendToAddr.pop() #On fait du piggybagging
		print self.id, "envoi", seq, ack, data
		self.canalTransmission.sendto( pack( 'I', ((ack<<16)|seq) ) + data, addr )


	def sendSecure(self, data, addr):#N'envoi pas, va simplement mettre en attente le message.
		seq = random.randint(1, 0xFFFF)
		dataToSendToAddr = self.commDict.get(addr)
		if dataToSendToAddr:
			dataToSendToAddr.append((data, seq))
		else:
			self.commDict[addr] = [(data, seq)]

	def sendAllSecureQueued(self):
		for addr, dataToSendToAddr in self.commDict.iteritems():
			if dataToSendToAddr:
				data = dataToSendToAddr[0]
				self.send(data[0], addr, data[1], 0)

	def sendAllPendingAck(self):
		for addr, listAck in self.ackDict.iteritems():
			while listAck:
				ack = listAck.pop()
				self.send( "", addr, 0, ack )

	def listen(self):
		data = None
		addr = None

		#Pour avancer, il faut recevoir un message qui ne contienne pas qu'un ack
		while data == None:
			##TOUTES LES 30[ms] ON ENVOI LES MESSAGES SECURISE ET ON ACK LES ACK NON PIGGYBAGGE##
			for event in pygame.event.get():
				if event.type == USEREVENT+1:
					self.sendAllSecureQueued() #calling the function wheever we get timer event.
					self.sendAllPendingAck()

			data, addr = self.canalTransmission.receive( 0 ) #non bloquant
			
			if(data != None):
				##ON PREPARE AU TRAITEMENT LES DONNEES RECU##
				bytes = unpack( 'I', data[0:4] )
				bytes = bytes[0]
				data = data[4:]
				if data == "":
					data = None
				bytesT = bytes
				ack = ( (bytes&0xFFFF0000) >> 16 ) #Numero de sequence qu'on va devoir ack
				seq = bytesT&0x0000FFFF #Numero d'ack qui confirme un envoi securise
				print self.id, "recoi", seq, ack, data

				##TRAITEMENT DU ACK SI IL EST PLUS GRAND QUE ZERO##
				if ( ack>0 ):
					dataToSendToAddr = self.commDict.get( addr )#Recupere la liste de donne a envoyer a addr
					if dataToSendToAddr:
						dataToSendToAddr = [(dat, sequence) for dat, sequence in dataToSendToAddr if sequence != ack]#Retourne la liste moins l'element confirme
						self.commDict[addr] = dataToSendToAddr

				##TRAITEMENT DE LA SEQUENCE SI ELLE EST PLUS GRAND QUE ZERO##
				if ( seq>0 ):
					AckToSendToAddr = self.ackDict.get( addr )
					if AckToSendToAddr != None:
						AckToSendToAddr.append( seq )
					else:
						self.ackDict[addr] = [seq]

		return ( data, addr )
