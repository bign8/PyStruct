import sys
from net import lib
from time import sleep

msg = " ".join(sys.argv[1:])


def start():
    sock = lib.init()
    try:
        sock.send('S')
        message = lib.get(sock)
    finally:
        sock.close()

    return message


def ping():
    sock, msg = None, 'PING'
    try:
        sock = lib.init()
        sock.send('P')
        msg = lib.get(sock)
    except lib.socket.error:
        pass
    finally:
        if sock:
            sock.close()
    return msg == 'PONG'


class Delay(object):
    past = 1
    now = 1

    def __call__(self):
        print 'Sleeping for {}s'.format(self.now)
        sleep(self.now)
        self.past, self.now = self.now, self.now + self.past


if __name__ == '__main__':
    delay = Delay()
    while True:
        try:
            if not ping():
                delay()
                continue

            print start()
            sleep(10)
            lib.end(float(msg), {
                'asdf': ['asd', 'ssdfg'],
                'regqer': ['as', 'sfdgn']
            })
        except lib.socket.error:
            pass
