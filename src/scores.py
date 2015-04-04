from math import log
from data import DataSet
from models import EntityCache


def K(X_i, PA_i):
    """
    :type X_i: :class:`data.Variable`
    :type PA_i: set
    :rtype: float
    """
    items = [len(x_l.domain) for x_l in PA_i]
    return (len(X_i.domain) - 1) * reduce(lambda x, y: x * y, items, 1)


# def penalty_mdl(X_i, B, D):
#     """
#     Compute the MDL penalty of a given node, see page 17 of the text.
#
#     :param X_i: The Variable to be analyzed
#     :type X_i: :class:`data.Node`
#     :param B: Some data we are given
#     :type B: ???
#     :param D: The dataset this is over
#     :type D: :class:`.data.DataSet`
#     :return: The MDL penalty associated with this node
#     :rtype: float
#     """
#     # Based on equation penaltyMDL 2.6
#     return log(len(D.data)) * len(X_i.vars) * 1.0 / 2
#
#
# def log_likelihood(D, B):
#     """
#     Compute the log likelihood of D given B, see page 16 of the text.
#
#     :param D: The dataset this is over
#     :type D: :class:`.data.DataSet`
#     :param B: Some data we are given
#     :type B: ???
#     :return: The log-likelihood of D given B
#     :rtype: float
#     """
#     # by equation 2.3
#     result = sum([log(D.probability_given(D_j, B)) for D_j in D.data])
#
#     # by equation 2.4
#     # ???
#
#     return result
#
#
# def decomposable_penalized_log_likelihood(B, D):
#     """
#     Compute DPLL, see page 16 of the text.
#
#     :param B: Some data we are given
#     :type B: ???
#     :param D: The dataset this is over
#     :type D: :class:`.data.DataSet`
#     :return: The decomposable-penalized_log_likelihood
#     :rtype: float
#     """
#     penalty = sum([penalty_mdl(X_i, B, D) for X_i in D.data])
#     return log_likelihood(D, B) + penalty
#
#
# score = decomposable_penalized_log_likelihood


"""  ------------------- Algorithms from Table 4.6 -----------------------  """


class BN(DataSet):
    score = EntityCache()
    best_score = EntityCache()
    base_score = {}

    def find_consistent_records(self, X_i, value, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type value: object
        :type D_u: set
        :rtype: set
        """
        idxs = self.magic[X_i][value]
        return idxs.intersection(D_u)
        # idx = self.variables.index(X_i)
        # return [item for item in D_u if item[idx] == value]

    def build_record_slices(self):
        # Populate datas tructure with the data indexes
        self.magic = {}
        for data_idx, record in enumerate(self.data):
            for idx, item in enumerate(record):
                top = self.magic.setdefault(self.variables[idx], dict())
                top.setdefault(item, set()).add(data_idx)

    def calculate_scores(self):
        print 'Updating Scores'
        self.update_scores(set(), self.data)
        self.expand_ad_node(-1, set(), set(range(len(self.data))))
        print 'Prune Variables'
        for X in self.variables:
            self.prune(X, set(), self.score.get(X, set()))

    def expand_ad_node(self, i, U, D_u):
        """
        :type i: int
        :type U: set
        :type D_u: set
        """
        print 'Expanded AD node', i, U
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
            D_consistent_idx = self.find_consistent_records(X_i, value, D_u)
            D_consistent = [self.data[idx] for idx in D_consistent_idx]
            self.update_scores(U_union, D_consistent)
            N = len(self.data)
            if len(U) < log(2 * N / log(N)):
                self.expand_ad_node(self.variables.index(X_i), U_union, D_consistent_idx)

    def update_scores(self, U, D_u):
        """
        :type U: set
        :type D_u: list
        """
        D_size = len(D_u)
        delta = D_size * log(D_size) if D_size else 0
        for X in set(self.variables).difference(U):
            self.score.update(X, U, delta, K(X, U))
        for X in U:
            key = U.difference({X})
            self.score.update(X, key, -delta, K(X, key))

    def prune(self, Y, U, best_score):
        """
        :type Y: :class:`.data.Variable`
        :type U: set
        :type best_score: float
        """
        for X in set(self.variables).difference(U):
            union = U.union({X})
            if self.score.get(X, union) < best_score:
                self.prune(Y, union, self.score.get(X, union))
            else:
                self.score.delete(X, union)
                self.prune(Y, union, best_score)
