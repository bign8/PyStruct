from __future__ import division
from time import time
from random import random


def main():
    hit = 0
    tot = 100000000L

    start = time()
    for _ in xrange(tot):
        x, y = random(), random()
        z = x * x + y * y  # sqrt
        if z <= 1:
            hit += 1
    stop = time()

    pi = hit / tot * 4
    print pi, stop - start

main()


def master():
