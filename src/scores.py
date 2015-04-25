import pickle
from os import path
from math import log
from models import EntityCache
from functools import partial
from progress import Bar
from time import time


PRUNE_CAP = 5e7


prod = lambda items: reduce(lambda x, y: x * y, items, 1)

"""
Algorithms from Table 4.6
"""


def K(X_i, PA_i):
    """
    :type X_i: :class:`data.Variable`
    :type PA_i: set
    :rtype: float
    """
    items = [len(x_l.domain) for x_l in PA_i]
    return (len(X_i.domain) - 1) * prod(items)


class ScoreBuilder(object):

    def __init__(self, data, variables):
        """
        :type data: list[list]
        :type variables: list[:class:`data.Variable`]
        """
        self.N = len(data)
        self.score = EntityCache()
        self.variables = variables
        self.vset = frozenset(variables)

        # Pre-build slices
        self.slices = dict()
        self.build_record_slices(data)

    def build_record_slices(self, data):
        """ Populate data structure with the data indexes """
        for data_idx, record in enumerate(data):
            for idx, item in enumerate(record):
                variable = self.variables[idx]
                top = self.slices.setdefault(variable, dict())
                top.setdefault(variable.var_type(item), set()).add(data_idx)

    def __call__(self, name):
        file_path = path.abspath(path.join(
            path.dirname(__file__), 'data', name, '{}.score.p'.format(name)
        ))
        if path.isfile(file_path):
            # print 'Found Generated Scores - Loading'
            with open(file_path, 'rb') as f:
                self.score.cache = pickle.load(f)
        else:
            start = time()
            print 'Generating Score Cache'
            self.update_scores(set(), self.N)

            print 'Expanding Nodes'
            self.cap = log(2 * self.N / log(self.N))
            self.progress = Bar()
            expansion_count = self.count_node_expansions()
            self.progress.set_base(expansion_count, True)
            self.expand_ad_node(-1, set(), set(range(self.N)))

            print 'Prune Variables (Safe to kill)'
            try:
                prune_count = self.count_prune(set()) * len(self.variables)
                if prune_count < PRUNE_CAP:
                    self.progress.set_base(prune_count, True)
                    for X in self.variables:
                        self.prune(X, set(), self.score.get(X, set()))
                else:
                    print 'Skipping prune because >5e7 calls'
            except KeyboardInterrupt:
                print 'Killed pruning count due to keyboard interrupt'

            # clear negative scores
            for key, value in self.score.cache.iteritems():
                if value < 0:
                    self.score.cache[key] = 0
            stop = time()

            print 'Storing Generated Scored'
            with open(file_path, 'wb') as f:
                pickle.dump(self.score.cache, f)
            log_path = path.abspath(path.join(
                path.dirname(__file__), 'data', name, 'info.txt'
            ))
            with open(log_path, 'w') as f:
                f.write('Time: {}s\nExpansions: {}\nPrunes: {}'.format(
                    stop - start, expansion_count, prune_count
                ))

        return self.score

    def count_node_expansions(self, i=-1, depth=0):
        size = 1
        for variable in self.variables[i + 1:]:
            if depth < self.cap:
                count = self.count_node_expansions(
                    self.variables.index(variable), depth + 1
                )
                size += count * len(variable.domain)
            if size > PRUNE_CAP:
                return size
        return size

    def expand_ad_node(self, i, U, D_u):
        """
        :type i: int
        :param U: Node currently being expanded (set of Variables)
        :type U: set
        :param D_u: Indexes corresponding to the records consistent with U
        :type D_u: set
        """
        self.progress.increment()
        for variable in self.variables[i + 1:]:
            self.expand_vary_node(variable, U, D_u)

    def expand_vary_node(self, X_i, U, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type U: set
        :type D_u: set
        """
        U_union = U.union({X_i})
        for value in X_i.domain:
            D_idx = self.find_consistent_records(X_i, value, D_u)
            self.update_scores(U_union, len(D_idx))
            if len(U) < self.cap:
                self.expand_ad_node(self.variables.index(X_i), U_union, D_idx)

    def update_scores(self, U, D_size):
        """
        :type U: set
        :type D_u: int
        """
        if not D_size:
            return
        delta = D_size * log(D_size)
        for X in self.vset.difference(U):
            self.score.update(X, U, delta, partial(K, X, U))
        for X in U:
            key = U.difference({X})
            self.score.update(X, key, -delta, partial(K, X, key))

    _cache = set()

    def count_prune(self, U):
        U = frozenset(U)
        if U in self._cache:
            return 1
        size = 1
        for X in self.vset.difference(U):
            size += self.count_prune(U.union({X}))
        self._cache.add(U)
        return size

    _cache2 = set()

    def prune(self, Y, U, best_score):
        """
        :type Y: :class:`.data.Variable`
        :type U: set
        :type best_score: float
        """
        self.progress.increment()
        key = tuple([Y, frozenset(U)])
        if key in self._cache2:
            return
        for X in self.vset.difference(U):
            union = U.union({X})
            score = self.score.get(X, union)
            if score < best_score:
                self.prune(Y, union, score)
            else:
                self.score.delete(X, union)
                self.prune(Y, union, best_score)
        self._cache2.add(key)

    def find_consistent_records(self, X_i, value, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type value: object
        :type D_u: set
        :rtype: set
        """
        return self.slices[X_i][X_i.var_type(value)].intersection(D_u)
