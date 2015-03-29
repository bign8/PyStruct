import socket
from sys import stdin, stderr
from select import select
import Queue

from settings import PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORT))
server.listen(5)

running = True
inputs = [server, stdin]
outputs = []
message_queues = {}
names = {}


def close(client):
    inputs.remove(client)
    if client in outputs:
        outputs.remove(client)
    client.close()
    del message_queues[client]
    del names[client]


while running:
    print >>stderr, '\nwaiting for the next event'
    rlist, wlist, elist = select(inputs, outputs, inputs)

    for client in rlist:
        if client == server:
            new, addr = server.accept()
            print >>stderr, 'new connection from', addr
            new.setblocking(0)
            inputs.append(new)
            message_queues[new] = Queue.Queue()
            names[new] = addr
        elif client == stdin:
            junk = stdin.readline()
            running = False
        else:
            try:
                data = client.recv(1024)
            except socket.error:
                print >>stderr, 'socket closed', socket
                continue
            if data:
                print >>stderr, 'received', repr(data), 'from', names[client]
                message_queues[client].put(data)
                if client not in outputs:
                    outputs.append(client)
            else:
                print >>stderr, 'closing after reading no data'
                close(client)

    for client in wlist:
        try:
            next_msg = message_queues[client].get_nowait()
        except (Queue.Empty, KeyError):
            if client in outputs:
                print >>stderr, 'output queue for', names[client], 'is empty'
                outputs.remove(client)
        else:
            print >>stderr, 'sending', repr(next_msg), 'to', names[client]
            try:
                client.send(next_msg)
            except socket.error:
                print >>stderr, 'error sending to', names[client]

    for client in elist:
        print >>stderr, 'handling exceptional condition for', names[client]
        close(client)

for client in names:
    client.close()

server.close()
