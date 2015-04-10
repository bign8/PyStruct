from os import path


class DataSet(object):
    """
    A dataset (D) is a set of records (D_1 ... D_N), each of which is an
    instantiation of the variables in V.

    Variables (V) refer to the variables of the Bayesian network (`variables').
    """
    name = None
    data = None
    variables = None
    variable_map = None

    def __init__(self, name='scale'):
        """
        Load the dataset from file + instantiate variables as defined

        :param name: The name of the DataSet to be loaded
        :type name: str
        """
        self.name = name

        # Build variables list from file
        try:
            tmp = getattr(__import__('data.{}'.format(name)), name)
            self.variables = tmp.V
        except:
            pass  # will auto-generate variables later if necessary

        # Populate data instances and cast them as variables define
        self.data = []
        base_path = path.dirname(__file__)
        file_path = path.join(base_path, name, "{}.data".format(name))
        with open(path.abspath(file_path), 'rb') as handle:
            for line in handle:
                data, item = line.split(','), []

                # Generate variables if they aren't preset
                if not self.variables:
                    self.variables = [Variable() for _ in data]
                if len(self.variables) != len(data):
                    continue
                for variable, value in zip(self.variables, data):
                    # Skip null variables
                    if not variable:
                        continue
                    item.append(variable.process(value))
                self.data.append(item)

        # Prune null variables
        self.variables = [v for v in self.variables if v]
        self.variable_map = {v.name: v for v in self.variables}


class Variable(object):
    """
    A Variable (X_i \in V) is one of the variables of the Bayesian network.

    The states a variable can take on (r_i) is stored as `domain'
    """
    name = None
    domain = None
    var_type = None

    def __init__(self, name=None, var_type=str, domain=list()):
        self.name = name if name is not None else id(self)
        self.domain = set([var_type(x) for x in domain])
        self.var_type = var_type

    def process(self, value):
        item = self.var_type(value.strip())
        self.domain.add(item)
        return item

    def __repr__(self):
        return str(self.name)
