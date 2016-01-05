import os
import socket
import subprocess
import time
from snakeChan import SnakeChan
from snakePost import SnakePost

client = SnakeChan()
client.connect(("129.194.186.177", 8080))

time.sleep(1)

post = SnakePost(client, "client")

time.sleep(1)
print color.GREEN + "ok" + color.END