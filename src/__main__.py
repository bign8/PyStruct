from data import DataSet

if __name__ == '__main__':
    data = DataSet('scale')
    print data.probability('Class', 'L')
    print data.probability('Class', 'B')
    print data.probability('Class', 'R')
