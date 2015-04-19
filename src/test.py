from pprint import PrettyPrinter
from sys import argv
from base import procedure


if __name__ == '__main__':
    name = argv[1] if len(argv) > 1 else 'scale'
    score, graph = procedure(name)
    print 'Real Parent Graph'
    PrettyPrinter(indent=1).pprint(graph)
