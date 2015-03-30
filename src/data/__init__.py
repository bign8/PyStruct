from os import path


class DataSet(object):
    def __init__(self, name, variables=[]):
        self.name = name
        self.variables = variables
        self.variable_map = {v.name: v for v in variables}
        self.data = []
        self._cache = {}

    def process(self, fh):
        """
        Process the data associated with this dataset

        :param fh: File handle to file being processes
        :type fh: :class:`FILEHANDLE`
        :return: List of data values
        :rtype: list
        """
        results = []
        for line in fh:
            data, item = line.split(','), []
            for variable, value in zip(self.variables, data):
                item.append(variable.process(value))
            results.append(item)
        self.data = results
        return self

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
        if value not in self.variable_map.get(name).r:
            raise NameError('Value not available in Variable range')
        if name in self._cache:
            return self._cache.get(key)

        # Compute the probability of an instance happening in the DataSet
        total = len(self.data)
        count = 0
        idx = self.variables.index(self.variable_map.get(name))
        for item in self.data:
            if item[idx] == value:
                count += 1
        self._cache[key] = count * 1.0 / total
        return self._cache.get(key)


class Variable(object):
    def __init__(self, name, r=[], type=str):
        self.name = name
        self.r = r
        self.type = type

    def process(self, value):
        return self.type(value.strip())


class Node(object):
    def __init__(self, vars=[]):
        self.vars = vars


def load(name='scale'):
    """
    Load a specific set of data into a DataSet object

    :param name: The name of the DataSet to be loaded
    :type name: str
    :return: A preloaded DataSet
    :rtype: :class:`DataSet`
    """
    tmp = getattr(__import__('data.{}'.format(name)), name)
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, name, "{}.data".format(name))
    handle = open(path.abspath(filepath), 'rb')
    return DataSet(name, tmp.V).process(handle)
