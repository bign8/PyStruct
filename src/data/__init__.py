from os import path


class DataSet(object):
    """
    A dataset (D) is a set of records (D_1 ... D_N), each of which is an
    instantiation of the variables in V.

    Variables (V) refer to the variables of the Bayesian network (`variables').
    """
    def __init__(self, name='scale'):
        """
        Load the dataset from file + instantiate variables as defined

        :param name: The name of the DataSet to be loaded
        :type name: str
        """
        self.name = name
        self._probability_cache = {}  # probability cache

        # Build variables list from file
        tmp = getattr(__import__('data.{}'.format(name)), name)
        self.variables = tmp.V
        self.variable_map = {v.name: v for v in self.variables}

        # Populate data instances and cast them as variables define
        self.data = []
        base_path = path.dirname(__file__)
        file_path = path.join(base_path, name, "{}.data".format(name))
        with open(path.abspath(file_path), 'rb') as handle:
            for line in handle:
                data, item = line.split(','), []
                for variable, value in zip(self.variables, data):
                    item.append(variable.process(value))
                self.data.append(item)

    def build_forward_order_graph(self):
        pass

    def build_reverse_order_graph(self):
        graph = self.build_reverse_order_graph()
        # TODO: reverse graph links
        return graph

    def probability(self, name, value):
        """
        Compute the probability of a Variable being a Value

        :param name: The name of the variable we are looking for
        :type name: basestring
        :param value: The value of the variable we are looking for
        :type value: basestring
        :return: Probability of `variable' being a `value'
        :rtype: float
        """
        key = '{}-{}'.format(name, value)

        if name not in self.variable_map:
            raise AttributeError('Variable not available')
        if value not in self.variable_map.get(name).domain:
            raise NameError('Value not available in Variable range')

        # Compute the probability of an instance happening in the DataSet
        if name not in self._probability_cache:
            total = len(self.data)
            count = 0
            idx = self.variables.index(self.variable_map.get(name))
            for item in self.data:
                if item[idx] == value:
                    count += 1
            self._probability_cache[key] = count * 1.0 / total

        return self._probability_cache.get(key)

    def probability_given(self, a, b):
        # TODO: implement this
        pass


class Variable(object):
    """
    A Variable (X_i \in V) is one of the variables of the Bayesian network.

    The states a variable can take on (r_i) is stored as `domain'
    """
    def __init__(self, name, domain=list(), var_type=str):
        self.name = name
        self.domain = [var_type(x) for x in domain]
        self.var_type = var_type

    def process(self, value):
        return self.var_type(value.strip())

    def __repr__(self):
        return self.name


class Node(object):
    """
    A node is a node in the search graph and corresponds to a set of variables.
    Typically represented in the text by a bold upper-case letter, and can
    refer to either the set of variables, or the node itself depending on context.
    """
    def __init__(self, var_set=list()):
        self.var_set = var_set
