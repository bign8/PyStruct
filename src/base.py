from models import Timer
from search import BNSearch
from scores import ScoreBuilder


def procedure(name, weight=1, monitor=None):
    timer = Timer('Fetching Variables')
    data = BNSearch(name)
    print timer.stop()

    timer = Timer('Calculate Scores')
    data.score = ScoreBuilder(data.data, data.variables)(data.name)
    print timer.stop()

    if monitor:
        monitor.start()
    timer = Timer('Search')
    try:
        score = data.search(weight, monitor=monitor)
    finally:
        print timer.stop()
        if monitor:
            monitor.stop()

    timer = Timer('REBUILD graph (sorry Bruce Wayne)')
    graph = data.build_graph()
    print timer.stop()

    return score, graph
