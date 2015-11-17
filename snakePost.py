from Color import color
from snakeChan import SnakeChan


class snakePost:

    def __init__(self, snakeChan = None):
        self.chan = snakeChan
        print color.GREEN + "snakePost instanciated." + color.END


    def send(self, com, data):
        return True

    def receive(self, com):
        return True
