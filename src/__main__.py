from net import lib
from search import BNSearch
from scores import ScoreBuilder
from models import Timer


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

            # Clean graph for transport
            clean = {}
            for key, value in graph.iteritems():
                clean[key.name] = ','.join(v.name for v in value)

            print 'Finish "{}" with score  of {:.4f}'.format(name, score)
            lib.end(name, weight, score, clean)
        except lib.socket.error:
            pass
        except KeyboardInterrupt:
            break
