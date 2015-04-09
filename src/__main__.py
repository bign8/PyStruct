from search import BNSearch
from scores import ScoreBuilder
from models import Timer
import pprint
import json


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
    # data = BNSearch('scale')
    data = BNSearch('flag')
    print timer.stop()

    timer = Timer('Calculate Scores')
    data.score = ScoreBuilder(data.data, data.variables)()
    print timer.stop()
    # print json.dumps(data.score.cache)
    # exit()

    timer = Timer('Search')
    data.search()
    print timer.stop()

    timer = Timer('REBUILD graph (sorry Bruce Wayne)')
    parents = data.build_graph()
    print timer.stop()

    pp = pprint.PrettyPrinter(indent=1)
    print 'Real Parent Graph'
    pp.pprint(parents)
    # print json.dumps(data.came_from, cls=Encoder)
    # pp.pprint(data.score.cache)
    # pp.pprint(data.best_score.cache)
