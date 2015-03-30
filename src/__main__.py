from data import load

if __name__ == '__main__':
    data = load()
    print data.probability('Class', 'L')
    print data.probability('Class', 'B')
    print data.probability('Class', 'R')
