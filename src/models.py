from json import dumps

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
        return self.cache.get(frozenset(U), {}).get(X, default)

    def set(self, X, U, value):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type value: float
        """
        self.cache.setdefault(frozenset(U), {})[X] = value

    def delete(self, X, U):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        """
        data = self.cache.get(frozenset(U))
        if data and X in data:
            del data[X]

    def update(self, X, U, delta, default=0):
        """
        :type X: :class:`data.Variable`
        :type U: set or None
        :type delta: float
        """
        data = self.cache.setdefault(frozenset(U), {})
        data.setdefault(X, default)
        data[X] += delta


    def __repr__(self):
        return str(self.__dict__)
