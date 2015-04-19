import pickle
from os import path
from math import log
from models import EntityCache
from functools import partial
from progress import Bar


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
        self.vset = set(variables)

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

    def __call__(self, name, debug=False):
        file_path = path.abspath(path.join(
            path.dirname(__file__), 'data', name, '{}.score.p'.format(name)
        ))
        if path.isfile(file_path):
            if debug:
                print 'Found Generated Scores - Loading'
            with open(file_path, 'rb') as f:
                self.score.cache = pickle.load(f)
            if debug:
                print self.score
        else:
            if debug:
                print 'Generating Score Cache'
            self.update_scores(set(), self.N)

            if debug:
                print 'Expanding Nodes'
            self.cap = log(2 * self.N / log(self.N))
            self.progress = Bar()
            self.progress.set_base(self.count_node_expansions(), True)
            self.expand_ad_node(-1, set(), set(range(self.N)))

            if debug:
                print 'Prune Variables'
            self.progress.set_base(
                self.count_prune(set()) * len(self.variables), True
            )
            count = 0
            for X in self.variables:
                count = self.prune(X, set(), self.score.get(X, set()), count)

            # Fuck if I know
            for key, value in self.score.cache.iteritems():
                if value < 0:
                    self.score.cache[key] = 0

            if debug:
                print 'Storing Generated Scored'
            with open(file_path, 'wb') as f:
                pickle.dump(self.score.cache, f)

        return self.score

    def count_node_expansions(self, i=-1, depth=0):
        size = 1
        for variable in self.variables[i + 1:]:
            if depth < self.cap:
                count = self.count_node_expansions(
                    self.variables.index(variable), depth + 1
                )
                size += count * len(variable.domain)
        return float(size)

    def expand_ad_node(self, i, U, D_u, counter=0):
        """
        :type i: int
        :param U: Node currently being expanded (set of Variables)
        :type U: set
        :param D_u: Indexes corresponding to the records consistent with U
        :type D_u: set
        """
        counter += 1
        self.progress(counter)
        for variable in self.variables[i + 1:]:
            counter = self.expand_vary_node(variable, U, D_u, counter)
        return counter

    def expand_vary_node(self, X_i, U, D_u, counter):
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
                counter = self.expand_ad_node(
                    self.variables.index(X_i), U_union, D_idx, counter
                )
        return counter

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

    def count_prune(self, U):
        size = 1
        for X in self.vset.difference(U):
           size += self.count_prune(U.union({X}))
        return float(size)

    def prune(self, Y, U, best_score, counter=0):
        """
        :type Y: :class:`.data.Variable`
        :type U: set
        :type best_score: float
        """
        counter += 1
        self.progress(counter)
        for X in self.vset.difference(U):
            union = U.union({X})
            score = self.score.get(X, union)
            if score < best_score:
                counter = self.prune(Y, union, score, counter)
            else:
                self.score.delete(X, union)
                counter = self.prune(Y, union, best_score, counter)
        return counter

    def find_consistent_records(self, X_i, value, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type value: object
        :type D_u: set
        :rtype: set
        """
        return self.slices[X_i][X_i.var_type(value)].intersection(D_u)
