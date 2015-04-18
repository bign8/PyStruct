from time import time as now


class Timer(object):
    def __init__(self, name):
        self._line = '-'.join(['-'] * 10)
        print '{} Start: {} {}'.format(self._line, name, self._line)
        self.name = name
        self._start = now()
        self._stop = self._start

    def start(self):
        self._start = now()
        return self

    def stop(self):
        self._stop = now()
        print '{} Stop: {} {}'.format(self._line, self.name, self._line)
        return self

    def __repr__(self):
        return 'Timer "{}" ran for {:.4f}s'.format(
            self.name, self._stop - self._start
        )


def key(U, X):
    return tuple([frozenset(U), X])


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

    def __repr__(self):
        return str(self.__dict__)
