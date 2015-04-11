import sys
from net import lib
from time import sleep

score = float(" ".join(sys.argv[1:]))


if __name__ == '__main__':
    while True:
        try:
            name, weight = lib.start()
            print 'Starting search on {} with weight {}'.format(name, weight)
            sleep(10)  # simulating search
            print 'Ending search...'
            lib.end(name, weight, score, {
                'asdf': ['asd', 'ssdfg'],
                'regqer': ['as', 'sfdgn']
            })
        except lib.socket.error:
            pass
