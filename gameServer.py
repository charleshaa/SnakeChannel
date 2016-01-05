import time
from snakeChan import SnakeChan
from snakePost import SnakePost

serveur = SnakePost(SnakeChan('127.0.0.1', 3100), "serveur")
while 1:
	data = serveur.listen()
	if data[0] != None:
		if data[0] == "ping":
			serveur.sendSecure("ok", data[1])
		if data[0] == "re":
			serveur.sendSecure("caca", data[1])
		if data[0] == "kill":
			serveur.sendSecure("killed", data[1])
		if data[0] == "finished":
			serveur.sendSecure("bo", data[1])
		if data[0] == "boa":
			break