from progress import Bar
from models import EntityCache


class ParentBuilder(object):

    def __init__(self, data):
        self.data = data
        self.progress = Bar()
        self.best_score = EntityCache()
        self.vset = set(self.data.variables)

    def __call__(self):
        # TODO: cache parent graphs
        count = self.count_parent_graphs(self.data.variables[0], set())
        self.progress.set_base(count * len(self.data.variables), True)
        for X in self.data.variables:
            self.calculate_parent_graphs(X, set())
        self.progress.finish()

    def count_parent_graphs(self, Y, U):
        size = 1
        for X in self.vset.difference(U):
            union = U.union({X})
            size += self.count_parent_graphs(Y, union)
        return float(size)

    def calculate_parent_graphs(self, Y, U):
        self.progress.increment()
        for X in self.vset.difference(U):
            union = U.union({X})
            score = self.data.score.get(Y, union)
            if score is None:
                continue
            joint_union = self.data.joint_best_score(Y, union)[0]
            if score < self.data.joint_best_score(Y, U)[0] and score < joint_union:
                self.data.best_score.set(Y, union, score)
            elif self.data.best_score.get(Y, union) < joint_union:
                self.data.best_score.set(Y, union, score)
            self.calculate_parent_graphs(Y, union)
