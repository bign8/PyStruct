from os import path


class VariableSet(object):
    def __init__(self, variables=[]):
        self.variables = variables
        self.data = []

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


def load(name='data.scale'):
    short = name.split('.')[1]
    tmp = getattr(__import__(name), short)
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, short, "{}.data".format(short))
    handle = open(path.abspath(filepath), 'rb')
    return VariableSet(tmp.V).process(handle)
