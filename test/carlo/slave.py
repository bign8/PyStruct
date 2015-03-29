from settings import MASTER, PORT
from time import sleep
import socket

# attempt to open a connection to master:port
# listen for jobs + execute
# on failure send master failure message
# on master drop, console log and attempt to reconnect, backoff

class Delay:

    def __init__(self, cap=600, base=5, step=10):
        self.cap = cap
        self.base = base
        self.step = step
        self.current = self.base

    def wait(self):
        print 'Sleeping for {} seconds'.format(self.current)
        sleep(self.current)
        self.current += self.step
        if self.current > self.cap:
            self.current = self.cap

    def reset(self):
        self.current = self.base


pause = Delay()
running = True
while running:
    try:
        # Attempt to connect to master

    except:
        pass



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', PORT))

for i in xrange(10):
    s.send(b'hello, world!, {}'.format(i))
    data = s.recv(1024)
    print data
    sleep(2)

s.close()
