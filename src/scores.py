from math import log
from data import DataSet


def K(X_i, PA_i):
    """
    :type X_i: :class:`data.Variable`
    :type PA_i: set
    :rtype: float
    """
    items = [len(x_l.domain) for x_l in PA_i]
    return (len(X_i.domain) - 1) * reduce(lambda x, y: x * y, items, 1)


def penalty_mdl(X_i, B, D):
    """
    Compute the MDL penalty of a given node, see page 17 of the text.

    :param X_i: The Variable to be analyzed
    :type X_i: :class:`data.Node`
    :param B: Some data we are given
    :type B: ???
    :param D: The dataset this is over
    :type D: :class:`.data.DataSet`
    :return: The MDL penalty associated with this node
    :rtype: float
    """
    # Based on equation penaltyMDL 2.6
    return log(len(D.data)) * len(X_i.vars) * 1.0 / 2


def log_likelihood(D, B):
    """
    Compute the log likelihood of D given B, see page 16 of the text.

    :param D: The dataset this is over
    :type D: :class:`.data.DataSet`
    :param B: Some data we are given
    :type B: ???
    :return: The log-likelihood of D given B
    :rtype: float
    """
    # by equation 2.3
    result = sum([log(D.probability_given(D_j, B)) for D_j in D.data])

    # by equation 2.4
    # ???

    return result


def decomposable_penalized_log_likelihood(B, D):
    """
    Compute DPLL, see page 16 of the text.

    :param B: Some data we are given
    :type B: ???
    :param D: The dataset this is over
    :type D: :class:`.data.DataSet`
    :return: The decomposable-penalized_log_likelihood
    :rtype: float
    """
    penalty = sum([penalty_mdl(X_i, B, D) for X_i in D.data])
    return log_likelihood(D, B) + penalty


score = decomposable_penalized_log_likelihood


"""  ------------------- Algorithms from Table 4.6 -----------------------  """


class BN(DataSet):
    _score_cache = {}  # TODO: fix for threading

    """
    TODO: fix score cache to not be a two dimensional dictionary
    """
    def get_score(self, X, U):
        """
        :type X: :class:`data.Variable`
        :type U: set
        :rtype: float
        """
        return self._score_cache.get(frozenset(U), {}).get(X)

    def set_score(self, X, U, value):
        """
        :type X: :class:`data.Variable`
        :type U: set
        :type value: float
        """
        self._score_cache.setdefault(frozenset(U), {})[X] = value

    def find_consistent_records(self, X_i, value, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type value: object
        :type D_u: list
        :rtype: list
        """
        idx = self.variables.index(X_i)
        result = []
        for record in D_u:
            if record[idx] == value:
                result.append(record)
        return result

    def calculate_scores(self):
        self.update_scores(set(), self.data)
        self.expand_ad_node(-1, set(), self.data)
        for X in self.variables:
            self.prune(X, set(), self.get_score(X, set()))

    def expand_ad_node(self, i, U, D_u):
        """
        :type i: int
        :type U: set
        :type D_u: list
        """
        for variable in self.variables[i + 1:]:
            self.expand_vary_node(variable, U, D_u)

    def expand_vary_node(self, X_i, U, D_u):
        """
        :type X_i: :class:`data.Variable`
        :type U: set
        :type D_u: list
        """
        for value in X_i.domain:
            D_consistent = self.find_consistent_records(X_i, value, D_u)
            U_union = U.union({X_i})
            self.update_scores(U_union, D_consistent)
            N = len(self.data)
            if len(U) < log(2 * N / log(N)):
                self.expand_ad_node(self.variables.index(X_i), U_union, D_consistent)

    def update_scores(self, U, D_u):
        """
        :type U: set
        :type D_u: list
        """
        D_size = len(D_u)
        delta = D_size * log(D_size) if D_size else 0
        for X in set(self.variables).difference(U):
            if self.get_score(X, U) is None:
                self.set_score(X, U, K(X, U))
            self.set_score(X, U, self.get_score(X, U) + delta)
        for X in U:
            key = U.difference({X, })
            if self.get_score(X, key) is  None:
                self.set_score(X, key, K(X, key))
            self.set_score(X, U, self.get_score(X, key) - delta)

    def prune(self, Y, U, best_score):
        """
        :type Y: :class:`.data.Variable`
        :type U: set
        :type best_score: float
        """
        for X in set(self.variables).difference(U):
            union = U.union({X})
            if self.get_score(X, union) < best_score:
                self.prune(Y, union, self.get_score(X, union))
            else:
                self.set_score(X, union, None)
                self.prune(Y, union, best_score)
