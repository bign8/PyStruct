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


class EntityCache(object):
    """
    TODOs:
    * fix score cache to not be a two dimensional dictionary
    * fix _score_cache for threading
    """
    def __init__(self):
        self.cache = {}

    @staticmethod
    def _key(U):
        # TODO: use something better than a string
        names = sorted([u.name for u in U])
        return ','.join(names)

    def get(self, X, U, default=None):
        """
        :type X: :class:`data.Variable`
        :type U: set
        :rtype: float
        """
        return self.cache.get(self._key(U), {}).get(X.name, default)

    def set(self, X, U, value):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type value: float
        """
        self.cache.setdefault(self._key(U), {})[X.name] = value

    def delete(self, X, U):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        """
        data = self.cache.get(self._key(U))
        if data and X.name in data:
            del data[X.name]

    def update(self, X, U, delta, default=lambda: 0):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type delta: float
        :param default: using functools.partial can defer default calculation
        :type default: function
        """
        data = self.cache.setdefault(self._key(U), {})
        if X.name not in data:
            data[X.name] = default()
        data[X.name] += delta

    def __repr__(self):
        return str(self.__dict__)
