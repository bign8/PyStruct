from net import lib, models
from sys import argv
from base import procedure
from monitor import Monitor


def network():
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


if __name__ == '__main__':
    if len(argv) > 1:
        print procedure(argv[1])
    else:
        network()
