from time import sleep


class Delay:

    def __init__(self, cap=600, base=5, step=10):
        self.cap = cap
        self.base = base
        self.step = step
        self.current = self.base

    def __call__(self):
        print 'Sleeping for {} seconds'.format(self.current)
        sleep(self.current)
        self.current += self.step
        if self.current > self.cap:
            self.current = self.cap

    def reset(self):
        self.current = self.base
