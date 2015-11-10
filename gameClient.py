import time
from clientClass import Client



client = Client("Carlos", 3100)

client.send_message("I am a unicorn")

time.sleep(5)

client.send_message("Fuck this, I'm buying a Giraffe")

client.leave()
