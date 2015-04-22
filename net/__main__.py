from net import lib
from sys import argv
from random import choice
from SocketServer import TCPServer, BaseRequestHandler


class Memory(object):
    score = None
    graph = None
    name = None
    weight = None
    complete = False

    def __repr__(self):
        return str(self.__dict__)


class MyServer(TCPServer):
    data = dict()

    def save(self):
        # TODO: store data to disk
        pass


class MyTCPHandler(BaseRequestHandler):
    def get(self):
        return lib.get(self.request)

    def send(self, msg):
        lib.send(self.request, msg)

    def handle_start(self):
        name = argv[1] if len(argv) > 1 else None
        weight = 0
        if name:
            weights = [1.2, 1.1, 1.08, 1.04, 1]
            try:
                memory = self.server.data.setdefault(name, Memory())
                weight = choice([
                    w for w in weights
                    if not memory.weight or memory.weight > w
                ])
            except IndexError:
                name = None
        self.send((name, weight))

    def handle_end(self):
        name, weight, score, graph = self.get()
        data = self.server.data.setdefault(name, Memory())
        if weight < data.weight:
            data.weight = weight
            self.server.save()
        if data.score > score or not data.score:
            data.score = score
            data.graph = graph
            data.weight = weight
            data.name = name
            print 'New best score of {} for {}'.format(score, name)
            if weight <= 1:
                print 'Completed Search on {}'.format(name)
                data.complete = True
            self.server.save()
        else:
            print 'Worse score of {} for {}'.format(score, name)

    def handle_get(self):
        data = self.server.data.setdefault(self.get(), Memory())
        self.send((data.score, data.complete))

    def handle_ping(self):
        self.send('PONG')

    def handle(self):
        obj = {
            'S': self.handle_start,
            'E': self.handle_end,
            'G': self.handle_get,
            'P': self.handle_ping
        }
        command = self.request.recv(1)
        print 'Client {1}:{2} said "{0}"'.format(command, *self.client_address)
        if command in obj:
            obj.get(command, lambda: 0)()
        else:
            print '"{}" command not found'.format(command)

if __name__ == "__main__":
    server = MyServer((lib.HOST, lib.PORT), MyTCPHandler)
    print 'Serving at {}:{}'.format(*server.server_address)
    server.serve_forever()
