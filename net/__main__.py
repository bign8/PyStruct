import SocketServer
from net import lib


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def get(self):
        return lib.get(self.request)

    def send(self, msg):
        lib.send(self.request, msg)

    def handle_start(self):
        self.send((1.2, 'scale'))

    def handle_end(self):
        score, graph = self.get()
        if self.server.best_score > score or not self.server.best_score:
            self.server.best_score = score
            self.server.best_graph = graph
            print 'New best score of {}'.format(score)
        else:
            print 'Worse score of {}'.format(score)

    def handle_get(self):
        self.send(self.server.best)

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
    server = SocketServer.TCPServer((lib.HOST, lib.PORT), MyTCPHandler)
    server.best_score = None
    server.best_graph = None
    print 'Serving at {}:{}'.format(*server.server_address)
    server.serve_forever()
