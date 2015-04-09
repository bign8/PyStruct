# from UUID import uuid4
#
#
# class Node(object):
#     def __init__(self):
#         self._hash = uuid4().bytes
#
#     def __hash__(self):
#         return self._hash
#
#
# def neighbors(node):
#     return []
#
#
# def heuristic(node, goal):
#     return 0
#
#
# def dist(node, neighbor):
#     return 0
#
#
# def get_lowest_fscore(openset, f_score):
#     # return the node in openset having the lowest f_score[] value
#     keys = map(hash, openset)
#     subset = {key: f_score[key] for key in keys}
#     return min(subset, key=subset.get)
#
#
# def reconstruct(came_from, current):
#     total_path = [current]
#     while current in came_from:
#         current = came_from[hash(current)]
#         total_path.append(current)
#     return total_path
#
#
# def search(start, goal, epsilon=1):
#     closedset = set()  # The set of nodes already evaluated.
#     openset = set([start])  # The set of tentative nodes to be evaluated, initially containing the start node
#     came_from = {}  # The map of navigated nodes.
#
#     start_hash = hash(start)
#     g_score = {start_hash: 0}  # Cost from start along best known path.
#     # Estimated total cost from start to goal through y.
#     f_score = {}
#     f_score[start_hash] = g_score[start_hash] + epsilon * heuristic(start, goal)
#
#     while openset:
#         current = get_lowest_fscore(openset, f_score)
#         # current =
#         if current == goal:
#             return reconstruct(came_from, goal)
#
#         openset.remove(current)
#         closedset.add(current)
#         for neighbor in neighbors(current):
#             if neighbor in closedset:
#                 continue
#             tentative_g_score = g_score[hash(current)] + dist(current, neighbor)
#
#             n_hash = hash(neighbor)
#             if neighbor not in openset or tentative_g_score < g_score[n_hash]:
#                 came_from[n_hash] = current
#                 g_score[n_hash] = tentative_g_score
#                 f_score[n_hash] = tentative_g_score + epsilon * heuristic(neighbor, goal)
#                 if neighbor not in openset:
#                     openset.add(neighbor)
#     raise Exception('Path not found')
from data import DataSet
from itertools import chain, combinations
from models import EntityCache
from Queue import PriorityQueue


def powerset_generator(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield set(subset)


class BNSearch(DataSet):

    score = EntityCache()  # overridden in __main__
    best_score = EntityCache()
    base_score = {}
    parents = {}
    children = {}
    came_from = {}

    def search(self):
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
                print 'Number of expansions:', counter
                print 'The best score is', self.base_score.get(U)
                return
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
                print union, U, f
                if f < self.base_score.get(union, f + 1):
                    open.put((f, union))
                    self.base_score[union] = f
                    self.came_from[union] = U
                    self.parents[union] = parents
                    self.children[union] = X

    def build_graph(self):
        goal = frozenset(self.variables)

        parents, leaves = {}, {}

        while goal in self.children:
            parents[goal] = self.parents[goal]
            leaf = self.children[goal]
            leaves[goal] = leaf
            goal = goal.difference({leaf})

        real_graph = dict()
        for key in parents:
            real_graph[leaves[key]] = parents[key]

        return real_graph

    def joint_best_score(self, Y, U):
        diff = U.difference({Y})
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
