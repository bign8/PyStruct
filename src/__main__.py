from search import BNSearch
from time import time as now
import pprint


class Timer(object):
    def __init__(self, name):
        self.name = name
        self._start = now()
        self._stop = self._start

    def start(self):
        self._start = now()
        return self

    def stop(self):
        self._stop = now()
        return self

    def __repr__(self):
        return 'Timer "{}" ran for {:.4f}s'.format(
            self.name, self._stop - self._start
        )

if __name__ == '__main__':
    timer = Timer('Fetching Variables')
    data = BNSearch('scale')
    print timer.stop()

    timer = Timer('Sample Probability Calculations')
    print data.probability('Class', 'L')
    print data.probability('Class', 'B')
    print data.probability('Class', 'R')
    print timer.stop()

    timer = Timer('Calculate Scores')
    data.calculate_scores()
    print timer.stop()

    timer = Timer('Search')
    data.search()
    print timer.stop()

    pp = pprint.PrettyPrinter(indent=1)
    # pp.pprint(data.score.cache)
    # pp.pprint(data.best_score.cache)
