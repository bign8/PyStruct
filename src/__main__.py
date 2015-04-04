from search import BNSearch
from time import time as now
import pprint
import json


class Timer(object):
    def __init__(self, name):
        self.name = name
        self._start = now()
        self._stop = self._start

    def start(self):
        self._start = now()
        return self

    def stop(self):
        self._stop = now()
        return self

    def __repr__(self):
        return 'Timer "{}" ran for {:.4f}s'.format(
            self.name, self._stop - self._start
        )


# class Encoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, dict):
#             for key, value in obj.iteritems():
#
#
#         return json.JSONEncoder.default(self, obj)
#
#
# def _decode_list(data):
#     rv = []
#     for item in data:
#         if isinstance(item, unicode):
#             item = item.encode('utf-8')
#         elif isinstance(item, list):
#             item = _decode_list(item)
#         elif isinstance(item, dict):
#             item = _decode_dict(item)
#         rv.append(item)
#     return rv
#
#
# def _decode_dict(data):
#     rv = {}
#     for key, value in data.iteritems():
#         if isinstance(key, unicode):
#             key = key.encode('utf-8')
#         elif isinstance(key, (list, set, frozenset)):
#             key = '{!r}'.format(key)
#         if isinstance(value, unicode):
#             value = value.encode('utf-8')
#         elif isinstance(value, list):
#             value = _decode_list(value)
#         elif isinstance(value, dict):
#             value = _decode_dict(value)
#         rv[key] = value
#     return rv


if __name__ == '__main__':
    timer = Timer('Fetching Variables')
    data = BNSearch('scale')
    print timer.stop()

    # timer = Timer('Sample Probability Calculations')
    # print data.probability('Class', 'L')
    # print data.probability('Class', 'B')
    # print data.probability('Class', 'R')
    # print timer.stop()

    timer = Timer('Calculate Scores')
    data.calculate_scores()
    print timer.stop()

    timer = Timer('Search')
    data.search()
    print timer.stop()

    timer = Timer('Forward train BITCH')
    path = data.rebuild_forward_order_train()
    print timer.stop()

    timer = Timer('REBUILD actual parents (sorry Bruce Wayne)')
    parents = data.rebuild_parents(path[::-1])
    print timer.stop()

    pp = pprint.PrettyPrinter(indent=1)
    print 'parents'
    pp.pprint(parents)
    print 'path'
    pp.pprint(path)
    # print json.dumps(data.came_from, cls=Encoder)
    # pp.pprint(data.score.cache)
    # pp.pprint(data.best_score.cache)
