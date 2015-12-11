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

	def __init__(self, canalTransmission, ident):
		pygame.init()
		pygame.time.set_timer(USEREVENT+1, 30)
		self.canalTransmission = canalTransmission
		self.commDict = {}
		self.pendingAck = (None, None)
		self.id = ident
		print color.GREEN + "snakePost instanciated." + color.END

	def send(self, data, addr, seq=0):
		ack=0
		if self.pendingAck[0] == addr:
			ack = self.pendingAck[1]
			self.pendingAck = (None, None)
		print self.id, "envoi", seq, ack, data
		if addr != None:
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
				self.send(data[0], addr, data[1])

	def listen(self):
		data = None
		addr = None

		##TOUTES LES 30[ms] ON ENVOI LES MESSAGES SECURISE##
		for event in pygame.event.get():
			if event.type == USEREVENT+1:
				self.sendAllSecureQueued() #calling the function wheever we get timer event.
		
		if self.pendingAck[1] != None: #Si on a encore un ack a faire, on le fait
			self.send("", self.pendingAck[0])

		data, addr = self.canalTransmission.receive( 0 ) #non bloquant
		if data == "": ####!!!! We have to check if snakChan return None or "" if non data is received
				data = None
		if(data != None):
			##ON PREPARE AU TRAITEMENT LES DONNEES RECU##
			bytes = unpack( 'I', data[0:4] )
			bytes = bytes[0]
			data = data[4:]
			if data == "": ####!!!! We have to check if snakChan return None or "" if non data is received
				data = None
			bytesT = bytes
			ack = ( (bytes&0xFFFF0000) >> 16 ) #Numero d'ack qui confirme un envoi securise
			seq = bytesT&0x0000FFFF #Numero de sequence qu'on va devoir ack
			print self.id, "recoi", seq, ack, data

			##TRAITEMENT DU ACK SI IL EST PLUS GRAND QUE ZERO##
			if ( ack>0 ):
				dataToSendToAddr = self.commDict.get( addr )#Recupere la liste de donne a envoyer a addr
				if dataToSendToAddr:
					dataToSendToAddr = [(dat, sequence) for dat, sequence in dataToSendToAddr if sequence != ack]#Retourne la liste moins l'element confirme
					self.commDict[addr] = dataToSendToAddr

			##TRAITEMENT DE LA SEQUENCE SI ELLE EST PLUS GRAND QUE ZERO##
			if ( seq>0 ):
				self.pendingAck = (addr, seq)
				dataToSendToAddr = self.commDict.get(addr)
				if dataToSendToAddr:
					print "ICI"
					data = dataToSendToAddr[0]
					self.send(data[0], addr, data[1])

		return ( data, addr )
