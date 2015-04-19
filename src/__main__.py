from net import lib, models
from threading import Thread, Event
from base import procedure


class Monitor(Thread):
    def __init__(self, **kwargs):
        super(Monitor, self).__init__(**kwargs)
        self.complete = False
        self.score = 1e9
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            score, self.complete = lib.update(self.name)
            if score:
                self.score = score
            self.event.wait(10)

    def stop(self):
        print 'Killing monitor'
        self.event.set()
        self.join()


if __name__ == '__main__':
    delay = models.Delay()
    while True:
        try:
            name, weight = lib.start()
            if not name:
                print 'No job'
                delay()
                continue
            else:
                delay.reset()
            print 'Search "{}" with weight of {:.6f}'.format(name, weight)

            score, graph = procedure(name, weight, Monitor(name=name))

            print 'Finish "{}" with score  of {:.4f}'.format(name, score)
            lib.end(name, weight, score, graph)
        except lib.socket.error:
            pass
        except KeyboardInterrupt:
            break
