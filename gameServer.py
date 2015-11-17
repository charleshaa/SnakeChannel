import time
from snakeChan import SnakeChan

serveur = SnakeChan(3100)
while 1:
	data = serveur.receive(0)
	if data != None:
		print data