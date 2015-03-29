from UUID import uuid4

class Node(object):
    def __init__():
        self._hash = uuid4().bytes

    def __hash__(self):
        return self._hash


def neighbors(node):
    return []


def heuristic(node, goal):
    return 0


def dist(node, neighbor):
    return 0


def get_lowest_fscore(openset, f_score):
    # return the node in openset having the lowest f_score[] value
    keys = map(hash, openset)
    subset = {key: f_score[key] for key in keys}
    return min(subset, key=subset.get)



def reconstruct(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[hash(current)]
        total_path.append(current)
    return total_path


def search(start, goal, epsilon=1):
    closedset = set()  # The set of nodes already evaluated.
    openset = set([start])  # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = {}  # The map of navigated nodes.

    start_hash = hash(start)
    g_score = {start_hash: 0}  # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start_hash] = g_score[start_hash] + epsilon * heuristic(start, goal)

    while openset:
        current = get_lowest_fscore(openset, f_score)
        # current =
        if current == goal
            return reconstruct(came_from, goal)

        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbors(current):
            if neighbor in closedset
                continue
            tentative_g_score = g_score[hash(current)] + dist(current, neighbor)

            n_hash = hash(neighbor)
            if neighbor not in openset or tentative_g_score < g_score[n_hash]
                came_from[n_hash] = current
                g_score[n_hash] = tentative_g_score
                f_score[n_hash] = tentative_g_score + epsilon * heuristic(neighbor, goal)
                if neighbor not in openset
                    openset.add(neighbor)

    raise Exception('Path not found')
