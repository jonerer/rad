# -*- coding: utf-8 -*
import socket, threading, sys, select
from Queue import Queue

client_sockets = {}

out_queue = {}
out_buffer = {}

in_queue = {}
in_buffer = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 443))
s.setblocking(0)
s.settimeout(0)
s.listen(5)

while True:
    try:
        acceptor = select.select([s,], [s,], [s,], 0)[0]
        if acceptor:
            newsocket, addr = s.accept()
            client_sockets[newsocket.fileno()] = newsocket
            out_queue[newsocket.fileno()] = Queue()
            out_buffer[newsocket.fileno()] = ""
            in_buffer[newsocket.fileno()] = Queue()
            in_queue[newsocket.fileno()] = ""
            print "new connected %s: %s, %s" % (newsocket.fileno(), newsocket, addr)
            print client_sockets

        read_list, write_list, error_list = select.select(
            client_sockets.values(),
            client_sockets.values(),
            client_sockets.values(), 1)

        for sock in read_list:
            # TODO: fixa in_buffern :p
            # och in_queue
            print "läsa från %s" % sock.fileno()
            read = sock.recv(1024)
            if read != "":
                print "lägger till %s" % read
                for fileno, target_queue in out_queue.iteritems():
                    if sock.fileno() != fileno:
                        target_queue.put("%s hälsar: %s" % (client_sockets, read))

        for sock in write_list:
            if out_buffer[sock.fileno()] == "" and \
                not out_queue[sock.fileno()].empty():
                print "ska skriva till.... %s" % sock.fileno()
                out_buffer[sock.fileno()] = out_queue[sock.fileno()].get()

            if out_buffer[sock.fileno()] != "":
                sent = sock.send(out_buffer[sock.fileno()])
                if sent != len(out_buffer[sock.fileno()]):
                    out_buffer[sock.fileno()] = out_buffer[sock.fileno()][sent:]

        for sock in error_list:
            print "fel på %s" % sock.fileno()
    except (KeyboardInterrupt, socket.error):
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        for sock in client_sockets.values():
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

