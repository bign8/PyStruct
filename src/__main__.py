from net import lib
from search import BNSearch
from scores import ScoreBuilder
from models import Timer


if __name__ == '__main__':
    # TODO: add another thread to watch for updated scores
    while True:
        try:
            name, weight = lib.start()

            timer = Timer('Fetching Variables')
            data = BNSearch(name)
            print timer.stop()

            timer = Timer('Calculate Scores')
            data.score = ScoreBuilder(data.data, data.variables)(data.name)
            print timer.stop()

            timer = Timer('Search')
            score = data.search(weight)
            print timer.stop()

            timer = Timer('REBUILD graph (sorry Bruce Wayne)')
            graph = data.build_graph()
            print timer.stop()

            lib.end(name, weight, score, graph)
        except lib.socket.error:
            pass
