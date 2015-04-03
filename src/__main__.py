from search import BNSearch
import pprint

if __name__ == '__main__':
    data = BNSearch('scale')
    print data.probability('Class', 'L')
    print data.probability('Class', 'B')
    print data.probability('Class', 'R')
    data.calculate_scores()
    data.search()

    pp = pprint.PrettyPrinter(indent=1)
    # pp.pprint(data.score.cache)
    # pp.pprint(data.best_score.cache)
