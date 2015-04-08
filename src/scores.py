from math import log
from models import EntityCache
from functools import partial

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
    return (len(X_i.domain) - 1) * reduce(lambda x, y: x * y, items, 1)


class ScoreBuilder(object):

    def __init__(self, data, variables):
        """
        :type data: list[list]
        :type variables: list[:class:`data.Variable`]
        """
        self.N = len(data)
        self.score = EntityCache()
        self.variables = variables  # TODO: sort based on domain size
        self.vset = set(variables)

        # Pre-build slices
        self.slices = dict()
        self.build_record_slices(data)

    def build_record_slices(self, data):
        """ Populate data structure with the data indexes """
        for data_idx, record in enumerate(data):
            for idx, item in enumerate(record):
                top = self.slices.setdefault(self.variables[idx], dict())
                top.setdefault(item, set()).add(data_idx)

    def __call__(self):
        print 'Updating Scores'
        self.update_scores(set(), self.N)

        print 'Expanding Nodes'
        self.expand_ad_node(-1, set(), set(range(self.N)))

        print 'Prune Variables'
        for X in self.variables:
            self.prune(X, set(), self.score.get(X, set()))

        return self.score

    def expand_ad_node(self, i, U, D_u):
            """
            :type i: int
            :param U: Node currently being expanded (set of Variables)
            :type U: set
            :param D_u: Indexes corresponding to the records consistent with U
            :type D_u: set
            """
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
            if len(U) < log(2 * self.N / log(self.N)):
                self.expand_ad_node(self.variables.index(X_i), U_union, D_idx)

    def update_scores(self, U, D_size):
        """
        :type U: set
        :type D_u: int
        """
        delta = D_size * log(D_size) if D_size else 0
        for X in self.vset.difference(U):
            self.score.update(X, U, delta, partial(K, X, U))
        for X in U:
            key = U.difference({X})
            self.score.update(X, key, -delta, partial(K, X, key))

    def prune(self, Y, U, best_score):
        """
        :type Y: :class:`.data.Variable`
        :type U: set
        :type best_score: float
        """
        for X in self.vset.difference(U):
            union = U.union({X})
            if self.score.get(X, union) < best_score:
                self.prune(Y, union, self.score.get(X, union))
            else:
                self.score.delete(X, union)
                self.prune(Y, union, best_score)

    def find_consistent_records(self, X_i, value, D_u):
            """
            :type X_i: :class:`data.Variable`
            :type value: object
            :type D_u: set
            :rtype: set
            """
            return self.slices[X_i][value].intersection(D_u)
