from data import DataSet
from itertools import chain, combinations
from models import EntityCache
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
        self.best_score = EntityCache()
        self.base_score = {}
        self.parents = {}
        self.leaves = {}

    def search(self, weight=1, debug=False):
        """
        :type D: :class:`scores.BN`
        """
        open = PriorityQueue()
        closed = set()

        # Calculate parent graph
        for X in self.variables:
            self.calculate_parent_graphs(X, set())

        variables = set(self.variables)
        open.put((1, frozenset()))
        counter = 0
        while not open.empty():
            counter += 1
            U = open.get()[1]
            if U == frozenset(self.variables):
                if debug:
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
                f = g + h
                if debug:
                    print union, U, f
                if f < self.base_score.get(union, f + 1):
                    open.put((f, union))
                    self.base_score[union] = f
                    self.parents[union] = parents
                    self.leaves[union] = X
        raise Exception('Search Cannot Find Goal')

    def build_graph(self):
        goal, graph = frozenset(self.variables), {}
        while goal in self.leaves:
            leaf = self.leaves[goal]
            graph[leaf.name] = ','.join(v.name for v in self.parents[goal])
            goal = goal.difference({leaf})
        return graph

    def joint_best_score(self, Y, U):
        diff = U.difference({Y})
        # TODO: ensure this logic is correct
        if len(U) < 2:
            return self.score.get(Y, diff), diff
        return min(
            [
                (self.score.get(Y, parents), parents)
                for parents in powerset_generator(diff)
            ], key=lambda x: x[0]
        )

    def calculate_parent_graphs(self, Y, U):
        for X in set(self.variables).difference(U):
            union = U.union({X})
            score = self.score.get(Y, union)
            if score is None:
                continue
            joint_union = self.joint_best_score(Y, union)[0]
            if score < self.joint_best_score(Y, U)[0] and score < joint_union:
                self.best_score.set(Y, union, score)
            elif self.best_score.get(Y, union) < joint_union:
                self.best_score.set(Y, union, score)
            self.calculate_parent_graphs(Y, union)
