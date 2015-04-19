from os import environ
from sys import stdout


class Bar(object):
    def __init__(self):
        _, self.width = get_terminal_size()
        self.width -= 14
        self.base = -1

    def set_base(self, base, debug=False):
        if debug:
            print 'Progress cap set at {}'.format(base)
        self.base = base

    def __call__(self, count):
        percent = count / self.base
        fin = int(percent * self.width)
        remain = self.width - fin
        bar = ''.join([u'\u2588'] * fin) + ''.join(['-'] * remain)
        stdout.write(u'[ {} ]{:>8.2f}%\r'.format(bar, percent * 100))
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
