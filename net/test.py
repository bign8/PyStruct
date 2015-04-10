import socket
import sys
import pickle

HOST, PORT = "localhost", 9991
data = " ".join(sys.argv[1:])


def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        sock.sendall('S')
        message_length = sock.recv(8)
        message = sock.recv(int(message_length))
    finally:
        sock.close()

    return pickle.loads(message)


def end():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        sock.sendall('E')
        data = pickle.dumps({
            'S': 10000,
            'G': {
                'asdf': ['asd', 'ssdfg'],
                'regqer': ['as', 'sfdgn']
            }
        })
        sock.sendall('{0:08d}'.format(len(data)) + data)
    finally:
        sock.close()

# TODO: make start smart enough to re-request for server (if dead)
print start()
end()
