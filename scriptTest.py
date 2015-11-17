import os
import socket
import subprocess
import time
from snakeChan import SnakeChan

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
client.send("ping")
data = client.receive(0)
if data[0] == "ok":
	print color.GREEN + "ok" + color.END
else:
	print color.RED + "error" + color.END

time.sleep(1)

print color.BOLD + "test system under pressur" +color.END
print "10 clients trying to connect with a loss rate of 20%, a delay of 500ms and a corruption of 10% (may take up to one minute)..."
for x in xrange(1,11):
  time.sleep(1)
  client = SnakeChan()
  os.system("sudo tc qdisc add dev lo root netem loss 20% delay 500 corrupt 10%")
  client.connect(("127.0.0.1", 3100))
  os.system("sudo tc qdisc del dev lo root netem")
  client.send("ping")
  data = client.receive(0)
  if data[0] == "ok":
    print color.GREEN + "client",x,"is ok" + color.END
  else:
    print color.RED + "client",x,"error" + color.END

os.system("pkill -9 python")