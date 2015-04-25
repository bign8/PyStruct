import json
from net import lib
from sys import argv
from time import time
from os.path import isfile
from SocketServer import TCPServer, BaseRequestHandler


class Memory(object):
    score = None
    graph = None
    weight = None
    complete = False
    start = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return str(self.__dict__)


STORE = 'data.json'


class MyServer(TCPServer):
    data = dict()
    processing = 1

    def __init__(self, *args, **kwargs):
        TCPServer.__init__(self, *args, **kwargs)
        if isfile(STORE):
            print 'Found previous run on disk. Loading + Restoring...'
            with open(STORE, 'r') as data:
                memories = json.load(data)
                for key, value in memories.iteritems():
                    memories[key] = Memory(**value)
                self.data = memories

    def save(self):
        data = {
            key: value.__dict__
            for key, value in self.data.iteritems()
        }
        print json.dumps(data, indent=4)
        with open(STORE, 'w') as bitch:
            json.dump(data, bitch, indent=4)


class MyTCPHandler(BaseRequestHandler):
    def get(self):
        return lib.get(self.request)

    def send(self, msg):
        lib.send(self.request, msg)

    def handle_start(self):
        name = None
        if len(argv) > self.server.processing:
            name = argv[self.server.processing]
        weight = 0
        if name:
            weights = [1.2, 1.1, 1.08, 1.04, 1]
            try:
                memory = self.server.data.setdefault(name, Memory())
                if memory.complete:
                    # If we are done, move on
                    self.server.processing += 1
                    return self.handle_start()

                weight = max([
                    w for w in weights
                    if not memory.weight or memory.weight > w
                ])
                if not memory.start:
                    memory.start = time()
            except Exception:
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
            print 'New best score of {} for {}'.format(score, name)
            if weight <= 1:
                print 'Completed Search on {}'.format(name)
                data.complete = True
                data.duration = time() - data.start
                del data.start
            self.server.save()
        else:
            print 'Worse score of {} for {}'.format(score, name)

    def handle_get(self):
        data = self.server.data.setdefault(self.get(), Memory())
        self.send((data.score, data.complete, data.weight))

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
        if command != 'P':
            print 'Client {1}:{2} said "{0}"'.format(
                command, *self.client_address
            )
        if command in obj:
            obj.get(command, lambda: 0)()
        else:
            print '"{}" command not found'.format(command)

if __name__ == "__main__":
    server = MyServer((lib.HOST, lib.PORT), MyTCPHandler)
    print 'Serving at {}:{}'.format(*server.server_address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Killing server'
        server.server_close()
        server.shutdown()
