import time
from snakeChan import SnakeChan
from snakePost import SnakePost

serveur = SnakePost(SnakeChan('127.0.0.1', 3100))
while 1:
	data = serveur.listen()
	if data[0] == "ping":
		serveur.sendSecure("ok", data[1])
