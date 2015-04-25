import pickle
import socket
from models import Delay
from os import environ


BUFF = 1024  # Size of initial buffer
PORT = 8880
HOST = '192.168.1.20'

# Development environment!
if environ.get('DEV'):
    PORT = 9994
    HOST = 'localhost'


def _init():
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


def _wait():
    """
    Waits until a connection to the server is available
    """
    def ping():
        sock, msg = None, 'PING'
        try:
            sock = _init()
            sock.send('P')
            msg = get(sock)
        except socket.error:
            pass
        finally:
            if sock:
                sock.close()
        return msg == 'PONG'

    delay = Delay()
    while not ping():
        delay()


def start():
    """
    Call to retrieve search from server
    :return: Dataset Name, Weight to use
    :rtype: str, float, float
    """
    _wait()
    sock = _init()
    try:
        sock.send('S')
        message = get(sock)
    finally:
        sock.close()

    return message


def end(name, weight, score, graph):
    """
    Called at the end of a search process
    :type name: str
    :type weight: float
    :type score: float
    :type graph: dict
    """
    _wait()
    sock = _init()
    try:
        sock.send('E')
        send(sock, (name, weight, score, graph))
    finally:
        sock.close()


def update(name):
    """
    Check the status of the search cluster
    :type name: str
    :return: score, complete, best_weight
    :rtype: float, bool, float
    """
    _wait()
    sock = _init()
    try:
        sock.send('G')
        send(sock, name)
        result = get(sock)
    finally:
        sock.close()
    return result
