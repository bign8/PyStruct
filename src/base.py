from models import Timer
from search import BNSearch
from scores import ScoreBuilder
from monitor import Monitor
# from parents import ParentBuilder


def procedure(name, weight=1, monitor=None):
    timer = Timer('Fetching Variables')
    data = BNSearch(name)
    print timer.stop()

    timer = Timer('Calculate Scores')
    data.score = ScoreBuilder(data.data, data.variables)(data.name)
    print timer.stop()

    # timer = Timer('Build Parent Graphs')
    # data.best_score = ParentBuilder(data)()
    # print timer.stop()

    if not monitor:
        monitor = Monitor()

    timer = Timer('Search')
    killed = False
    score = 1e99
    try:
        score = data.search(weight, monitor=monitor)
    except NotImplementedError, e:
        print 'Procedure {}:{} died with message: {}'.format(
            name, weight, e.message
        )
        killed = True
    finally:
        print timer.stop()

    if killed:
        return

    timer = Timer('REBUILD graph (sorry Bruce Wayne)')
    graph = data.build_graph()
    print timer.stop()

    return score, graph
