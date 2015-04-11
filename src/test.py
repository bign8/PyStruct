from search import BNSearch
from scores import ScoreBuilder
from models import Timer
from pprint import PrettyPrinter


if __name__ == '__main__':
    timer = Timer('Fetching Variables')
    data = BNSearch('flag')
    print timer.stop()

    timer = Timer('Calculate Scores')
    data.score = ScoreBuilder(data.data, data.variables)(data.name, debug=True)
    print timer.stop()

    timer = Timer('Search')
    data.search(debug=True)
    print timer.stop()

    timer = Timer('REBUILD graph (sorry Bruce Wayne)')
    parents = data.build_graph()
    print timer.stop()

    pp = PrettyPrinter(indent=1)
    print 'Real Parent Graph'
    pp.pprint(parents)
    # pp.pprint(data.score.cache)
    # pp.pprint(data.best_score.cache)
