from net import lib, models
from threading import Thread
from time import sleep
from base import procedure


class Monitor(Thread):
    def __init__(self, **kwargs):
        super(Monitor, self).__init__(**kwargs)
        self.complete = False
        self.score = 1e999
        self.kill_me = False

    def run(self):
        while not self.kill_me:
            self.score, self.complete = lib.update(self.name)
            sleep(10)

    def stop(self):
        self.kill_me = True
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
