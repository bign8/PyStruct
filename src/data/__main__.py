from sys import argv
import pickle
import gzip
from os import path


if __name__ == '__main__':
    if not argv or len(argv) < 2:
        print 'No name given'
        exit(1)

    name = argv[1]

    file_path = path.abspath(path.join(
        path.dirname(__file__), name, '{}.score.p'.format(name)
    ))

    new_file = path.abspath(path.join(
        path.dirname(__file__), name, 'score.pklz'
    ))

    print name, file_path

    if not path.isfile(file_path):
        print 'Input file does not exist:', file_path
        exit(1)

    if path.isfile(new_file):
        print 'Compressed file already exists:', new_file
        exit(1)

    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    with gzip.open(new_file, 'wb') as f:
        pickle.dump(data, f)
