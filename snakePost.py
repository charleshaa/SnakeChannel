import socket
import Queue
import random
import pygame
from pygame.locals import *
from Color import color
from struct import *
from snakeChan import SnakeChan


class SnakePost:

	def __init__(self, canalTransmission):
		pygame.init()
		self.canalTransmission = canalTransmission
		self.commList = []
		self.msgReceived = Queue.Queue() #Les messages recu sont mis en attente ici. 
		print color.GREEN + "snakePost instanciated." + color.END

	def send(self, data, addr, seq=0, ack=0):
		self.canalTransmission.sendto( pack( 'I', ((ack<<16)|seq) ) + data, addr )

	def sendSecure(self, data, addr):#N'envoi pas, va simplement mettre en attente le message.
		index=self.commIndex(addr)
		if ( index < 0 ):#Si on n'a jamais vu cette addr, on l'ajoute a notre liste, et on peut directement lui renvoyer un ack sans data
			self.commList.append( commData(addr) )
			index = self.commIndex( addr )
		self.commList[index].secureMsg( data, addr )

	def sendAllSecureQueued(self):
		for commData in self.commList:
			data = commData.getNextData()
			if data != None:
				self.send(data[0], data[1], data[2])

	def listen(self):
		data = None
		addr = None

		pygame.time.set_timer(USEREVENT+1, 30)

		#Pour avancer, il faut recevoir un message qui ne contienne pas qu'un ack
		while data == None:

			for event in pygame.event.get():
				if event.type == USEREVENT+1:
					self.sendAllSecureQueued() #calling the function wheever we get timer event.

			data, addr = self.canalTransmission.receive( 0 ) #non bloquant
			if(data != None):

				##ON PREPARE AU TRAITEMENT LES DONNEES RECU##
				bytes = unpack( 'I', data[0:4] )
				bytes = bytes[0]
				data = data[4:]
				if data == "":
					data = None
				ack = ( bytes&0xFFFF0000 ) >> 16 #Numero de sequence qu'on va devoir ack
				seq = bytes&0x0000FFFF #Numero d'ack qui confirme un envoi securise

				##RECUPERATION DE L'INDEX DU COMMUNICANT DANS NOTRE LISTE DE COMMUNICANT##
				index = self.commIndex(addr)

				##TRAITEMENT DU ACK SI IL EST PLUS GRAND QUE ZERO##
				if ( ack>0 ):
					if ( index < 0 ):
						raise Exception( "On recoi un ack pour un mec qu'on connait pas!" )
					self.commList[index].msgIsConfirm( ack )#on peut supprimer le message[ack] de la liste de msg securise a envoyer

				##TRAITEMENT DE LA SEQUENCE SI ELLE EST PLUS GRAND QUE ZERO##
				if ( seq>0 ):
					if ( index < 0 ):#Si on n'a jamais vu cette addr, on l'ajoute a notre liste, et on peut directement lui renvoyer un ack sans data
						self.commList.append( commData(addr) )
						index = self.commIndex( addr )
						self.send( "", addr, 0, seq )
					else:	#Si on connai cette addresse, on va recuperer l'eventuelle msg securise a envoyer a cette addr et on l'envoi avec l'ack du msg recu (piguibacking)
						dataSend = self.commList[index].getNextDataForAddr( addr )
						if dataSend:
							self.send( dataSend[0], addr, dataSend[1], seq )
						else:
							print dataSend
							self.send( "", addr, 0, seq)

		return ( data, addr )

	#############################
	#Retourne l'index du client dans clients[] en fonction de son tuple addresse (-1 si non trouve)
	#############################
	def commIndex(self, addr): 
		for index, commData in enumerate(self.commList):
			if commData.addr == addr:
				return index
		return -1

class commData:
	def __init__(self, addr):
		self.addr = addr
		self.msgSecure = []

	def secureMsg(self, msg, addr):
		seq = random.randint(1, 0xFFFF)
		self.msgSecure.append((msg, addr, seq))

	def msgIsConfirm(self, ack):
		self.msgSecure = [(msg, addr, seq) for msg, addr, seq in self.msgSecure if seq != ack]#Retourne la liste de msgSecurise moins le mesage confirme par le ack

	def getNextData(self):
		for data in self.msgSecure:
			return data

	def getNextDataForAddr(self, addr):
		data = [(msg, seq) for msg, addr, seq in self.msgSecure if addr == addr]#Extrait un message securise en attente d'envoi
		if not data:
			return ("", 0)#Si aucun message en attente
		else:
			return data#Si un message en attente
