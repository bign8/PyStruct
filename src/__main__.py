from scores import BN

if __name__ == '__main__':
    data = BN('scale')
    print data.probability('Class', 'L')
    print data.probability('Class', 'B')
    print data.probability('Class', 'R')
    data.calculate_scores()
    print data._score_cache
