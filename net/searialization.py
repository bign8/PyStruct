from settings import MESSAGE_SIZE
import pickle


def get(socket):
    length = int(socket.recv(MESSAGE_SIZE))
    return pickle.loads(socket.recv(length))


def send(socket, message):
    data = pickle.dumps(message)
    length_str = '{{0:0{}}}'.format(MESSAGE_SIZE).format(len(data))
    socket.sendall(length_str + data)
