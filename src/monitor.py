from net import lib
from threading import Thread, Event


class Monitor(Thread):
    def __init__(self, name):
        super(Monitor, self).__init__()
        self.name = name
        self.complete = False
        self.score = 1e9
        self.best = 2
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            score, self.complete, best = lib.update(self.name)
            if score:
                self.score = score
            if best:
                self.best = best
            self.event.wait(10)

    def stop(self):
        # print 'Killing monitor'
        self.event.set()
        self.join()
