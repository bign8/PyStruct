from data import DataSet
from itertools import chain, combinations
from models import EntityCache, key
from Queue import PriorityQueue


def powerset_generator(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield set(subset)


class BNSearch(DataSet):
    """
    TODO:
    - Delete data structures once they are no longer necessary
    """

    def __init__(self, name):
        super(BNSearch, self).__init__(name)
        self.score = EntityCache()
        self.base_score = {}
        self.parents = {}
        self.leaves = {}
        self._cache = {}

    def search(self, weight=1, monitor=False):
        """
        :type D: :class:`scores.BN`
        :type monitor: :class:`src.Monitor`
        """
        open = PriorityQueue()
        closed = set()

        print 'Beginning Search'
        variables = set(self.variables)
        open.put((1, frozenset()))
        counter = 0
        while not open.empty() and not monitor.complete:
            counter += 1
            U = open.get()[1]
            if U == frozenset(self.variables):
                print 'Number of expansions:', counter
                print 'The best score is', self.base_score.get(U)
                return self.base_score.get(U)
            closed.add(frozenset(U))
            for X in variables.difference(U):
                union = frozenset(U.union({X}))
                if union in closed:
                    continue
                # Score so far
                g, parents = self.joint_best_score(X, U)
                g += self.base_score.get(frozenset(U), 0)
                # Supposed next score
                h = sum(
                    self.joint_best_score(Y, variables.difference({Y}))[0]
                    for Y in variables.difference(U)
                )
                f = g + weight * h
                if f > monitor.score:
                    continue

                # print union, U, f
                if f < self.base_score.get(union, f + 1):
                    open.put((f, union))
                    self.base_score[union] = f
                    self.parents[union] = parents
                    self.leaves[union] = X

        if not monitor.complete:
            raise Exception('Search Cannot Find Goal')
        raise NotImplementedError('KILLED THIS BITCH')

    def build_graph(self):
        goal, graph = frozenset(self.variables), {}
        while goal in self.leaves:
            leaf = self.leaves[goal]
            graph[leaf.name] = ','.join(v.name for v in self.parents[goal])
            goal = goal.difference({leaf})
        return graph

    def joint_best_score(self, Y, U):
        index = key(U, Y)
        if index in self._cache:
            return self._cache[index]

        diff = U.difference({Y})
        # TODO: ensure this logic is correct
        if len(U) < 2:
            value = self.score.get(Y, diff), diff
        else:
            value = min(
                [
                    (self.score.get(Y, parents), parents)
                    for parents in powerset_generator(diff)
                ], key=lambda x: x[0]
            )
        self._cache[index] = value
        return value
