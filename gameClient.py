import time
from snakeChan import SnakeChan

client = SnakeChan()
client.connect(("127.0.0.1", 3100))
client.send("ping")
data = client.receive(0)
print data