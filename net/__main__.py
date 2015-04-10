import SocketServer
import pickle


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle_start(self):
        data = pickle.dumps({
            'W': 1000,
            'D': 'SHIT'
        })
        self.wfile.write('{0:08d}'.format(len(data)) + data)

    def handle_end(self):
        message_length = self.request.recv(8)
        message = self.request.recv(int(message_length))
        print pickle.loads(message)

    def handle(self):
        obj = {
            'S': self.handle_start,
            'E': self.handle_end
        }
        command = self.request.recv(1).strip()
        if command in obj:
            obj.get(command, lambda: 0)()
        else:
            print '"{}" command not found'.format(command)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9991

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
