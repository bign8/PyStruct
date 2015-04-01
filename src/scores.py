from math import log


def penalty_mdl(X_i, B, D):
    """
    Compute the MDL penalty of a given node, see page 17 of the text.

    :param X_i: The Variable to be analyzed
    :type X_i: :class:`.data.Node`
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
