from time import time as now
from progress import get_terminal_size


class Timer(object):
    def __init__(self, name):
        _, width = get_terminal_size()
        width = (width - len(name) - 2) // 2
        line = ''.join(['-'] * width)
        print '{0} {1} {0}'.format(line, name)
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


cache = {}


def key(U, X):
    fob = tuple([X, frozenset(U)])
    if fob in cache:
        return cache[fob]
    value = '{}:{}'.format('-'.join(sorted(u.name for u in U)), X.name)
    cache[fob] = value
    return value
    # return tuple([frozenset(U), X])


class EntityCache(object):
    """
    TODOs:
    * fix score cache to not be a two dimensional dictionary
    * fix _score_cache for threading
    """
    def __init__(self):
        self.cache = {}

    def get(self, X, U, default=None):
        """
        :type X: :class:`data.Variable`
        :type U: set
        :rtype: float
        """
        return self.cache.get(key(U, X), default)

    def set(self, X, U, value):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type value: float
        """
        self.cache[key(U, X)] = value

    def delete(self, X, U):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        """
        fob = key(U, X)
        if fob in self.cache:
            del self.cache[fob]

    def update(self, X, U, delta, default=lambda: 0):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type delta: float
        :param default: using functools.partial can defer default calculation
        :type default: function
        """
        fob = key(U, X)
        if fob not in self.cache:
            self.cache[fob] = default()
        self.cache[fob] += delta

    def contains(self, X, U):
        return key(U, X) in self.cache

    def __repr__(self):
        return str(self.__dict__)
