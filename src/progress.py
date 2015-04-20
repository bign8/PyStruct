from os import environ
from sys import stdout
from time import time


class Bar(object):
    def __init__(self):
        _, self.width = get_terminal_size()
        self.width -= 26
        self.base = -1
        self.last = -1
        self.count = 0

    def set_base(self, base, debug=False):
        if debug:
            print 'Progress cap set at {}'.format(base)
        self.base = float(base)
        self.start = time()
        self.count = 0

    def finish(self):
        self(self.base)

    def increment(self, count=1):
        self(self.count + count)

    def __call__(self, count):
        self.count = count
        percent = count / self.base
        new = int(percent * 10000)
        if new != self.last:
            self.last = new
            fin = int(percent * self.width)
            delta = time() - self.start
            remain = self.width - fin
            bar = ''.join([u'\u2588'] * fin) + ''.join(['-'] * remain)
            m, s = divmod(delta / percent - delta, 60)
            h, m = divmod(m, 60)
            stdout.write(
                u'[ {} ]{:>8.2f}% {:>2d}:{:02d}:{:05.2f}s\r'.format(
                    bar, percent * 100, int(h), int(m), s
                )
            )
            stdout.flush()
            if fin == self.width:
                print ''


def get_terminal_size(fd=1):
    """
    Returns height and width of current terminal. First tries to get
    size via termios.TIOCGWINSZ, then from environment. Defaults to 25
    lines x 80 columns if both methods fail.

    :param fd: file descriptor (default: 1=stdout)
    """
    try:
        import fcntl, termios, struct
        hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        try:
            hw = environ['LINES'], environ['COLUMNS']
        except:
            hw = (25, 80)
    return hw
