from threading import Thread
from time import sleep


class Monitor(Thread):
    def __init__(self, **kwargs):
        super(Monitor, self).__init__(**kwargs)
        self.complete = False
        self.score = 1e999
        self.kill_me = False

    def run(self):
        while not self.kill_me:
            # self.score, self.complete = update(self.name)
            self.score -= 1
            self.complete = not self.complete
            print self.kill_me
            sleep(10)


t = Monitor(name='bitches')
t.start()
try:
    while True:
        print t.score, t.complete
        sleep(5)

except KeyboardInterrupt:
    pass
print 'Killing...'

t.kill_me = True
t.join()
print t.score, t.complete
