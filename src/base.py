from models import Timer
from search import BNSearch
from scores import ScoreBuilder
from monitor import Monitor
# from parents import ParentBuilder


def procedure(name, weight=1, monitor=None, debug=True):
    timer = None
    if debug:
        timer = Timer('Fetching Variables')
    data = BNSearch(name)
    if debug:
        print timer.stop()
        timer = Timer('Calculate Scores')
    data.score = ScoreBuilder(data.data, data.variables)(data.name)
    if debug:
        print timer.stop()

    # timer = Timer('Build Parent Graphs')
    # data.best_score = ParentBuilder(data)()
    # print timer.stop()

    if not monitor:
        monitor = Monitor(name)

    if debug:
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
        if debug:
            print timer.stop()

    if killed:
        return

    graph = data.build_graph()
    return score, graph
