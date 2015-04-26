from sys import path
path.append('.')
from net import lib, models
from sys import argv
from base import procedure
from monitor import Monitor
from multiprocessing import cpu_count
from threading import Thread


class Process(Thread):
    def __init__(self, name, weight, monitor):
        super(Process, self).__init__()
        self.monitor = monitor
        self.name = name
        self.weight = weight
        self.score = None

    def run(self):
        score, graph = procedure(
            self.name, self.weight, self.monitor, debug=False
        )
        if score:
            self.score = score
            lib.end(self.name, self.weight, score, graph)


def network():
    delay = models.Delay(cap=5)
    while True:
        try:
            name, weight = lib.start()
            if not name:
                print 'No job'
                delay()
                continue
            else:
                delay.reset()
            print 'Search "{}" with max weight of {:.6f}'.format(name, weight)

            # Fire up process threads with shared access to monitor
            monitor = Monitor(name)
            monitor.start()
            threads = []
            # TODO: REMOVE TEMPORARY SINGLE THREADED HACK
            # thread_count, base = cpu_count(), 1
            # span = (weight - 1) / float(thread_count)
            # for _ in xrange(thread_count):
            #     thread = Process(name, base, monitor)
            #     base += span
            #     thread.start()
            #     threads.append(thread)
            thread = Process(name, weight, monitor)
            thread.start()
            threads.append(thread)

            # Use a round-robbin queue to ask the threads to join
            score = None
            counter = 0
            while threads:
                thread = threads[counter]
                thread.join(10)
                if not thread.is_alive():
                    threads.remove(thread)
                    if thread.score:
                        score = min(thread.score, score) if score else thread.score
                counter += 1
                if len(threads):
                    counter %= len(threads)
            monitor.stop()

            if score:
                print 'Finish "{}" with score  of {:.4f}'.format(name, score)
            else:
                print 'Other machine finished first, all cores dead'
        except lib.socket.error:
            pass
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    if len(argv) > 1:
        print procedure(argv[1])
    else:
        network()
