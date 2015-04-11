from net import lib
from search import BNSearch
from scores import ScoreBuilder


if __name__ == '__main__':
    # TODO: add another thread to watch for updated scores
    while True:
        try:
            name, weight = lib.start()
            print 'Search "{}" with weight of {:.6f}'.format(name, weight)

            data = BNSearch(name)
            data.score = ScoreBuilder(data.data, data.variables)(data.name)
            score = data.search(weight)
            graph = data.build_graph()

            print 'Finish "{}" with score  of {:.4f}'.format(name, score)
            lib.end(name, weight, score, graph)
        except lib.socket.error:
            pass
        except KeyboardInterrupt:
            break
