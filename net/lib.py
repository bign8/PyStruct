import pickle
import socket

# PORT = 8880
# MASTER = '192.168.1.20'
PORT = 9993
HOST = 'localhost'
BUFF = 1024  # Size of initial buffer


def init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except socket.error, e:
        sock.close()
        raise e
    return sock


def get(sock):
    length = int(sock.recv(BUFF))
    return pickle.loads(sock.recv(length))


def send(sock, message):
    data = pickle.dumps(message)
    length_str = '{{0:0{}}}'.format(BUFF).format(len(data))
    sock.sendall(length_str + data)


def end(score, graph):
    """
    Called at the end of a search process
    :type score: float
    :type graph: dict
    """
    sock = init()
    try:
        sock.send('E')
        send(sock, (score, graph))
    finally:
        sock.close()
