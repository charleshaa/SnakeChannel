import os
import socket
import subprocess
import time
from snakeChan import SnakeChan
from snakePost import SnakePost

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

print color.BOLD+"SnakeChan connection"+color.END, 

p = subprocess.Popen("python gameServer.py &", shell=True)
time.sleep(1)

client = SnakeChan()
client.connect(("127.0.0.1", 3100))

post = SnakePost(client)

post.sendSecure("ping", ("127.0.0.1", 3100))
while 1:
   data = post.listen()
   if data[0] == "ok":
      print color.GREEN + "ok" + color.END
      break;

os.system("pkill -9 python")
