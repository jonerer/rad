# -*- coding: utf-8 -*
import socket, threading, sys, select, struct, time
from Queue import Queue
from os import popen
from shared import buffrify, packet
from shared.data.serverdb import get_session, create_tables
from shared.data.serverdb.defs import *

print "gör session"
session = get_session()
print "gör tables"
create_tables()     
#Om du behöver fylla på databasen igen gör dessa nedanför
#skapar olika unittypes
#a=UnitType(u"Ambulans1", "static/ikoner/ambulans.png")
#b=UnitType(u"Brandbild1", "static/ikoner/brandbil.png")
#c=UnitType(u"sjukhus1", "static/ikoner/sjukhus.png")
#d=UnitType(u"jonas","static/ikoner/JonasInGlases.png")
#session.add(b)
#session.add(c)
#session.add(d)
#session.add(a)
#session.commit()
#skapar units
#session.add(Unit(u"hej", a, 15.57796, 58.40479))
#session.add(Unit(u"ho", a, 15.57806, 58.40579))
#session.add(Unit(u"lets", b, 15.5729, 58.40193))
#session.add(Unit(u"go", c, 15.5629, 58.4093))
#session.add(Unit(u"III", d, 15.5829, 58.4093, True))
#session.commit()
#Skapar användare
#session.add(User(u"jonas", u"mittlosen"))
#session.add(User(u"jon", u"supersecurepassword"))
#session.add(User(u"resman", u"superprogrammer"))
#session.add(User(u"Filho", u"jonas"))
#session.commit()

class Connection(object):
    
    pingtime = 3

    def __init__(self, socket, addr):
        self.addr, self.port = addr
        self.socket = socket
        self.id = socket.fileno()
        self.out_queue = Queue()
        self.out_buffer = ""
        self.in_queue = Queue()
        self.in_buffer = ""
        self.timestamp = time.time()
        self.timepinged = 0

client_sockets = {}
connections = {}
clientrequests = {}

def pong(connection, pack):
    print "Sätter ny timestamp"
    connection.timestamp = time.time()
    connection.timepinged = 0
clientrequests["pong"] = pong

def login(connection, pack): 
    loginaccept = True
    session.bind
    session.query(User).all()
    loginfo = pack.data
    username = loginfo["username"]
    password = loginfo["password"]
    for users in session.query(User).filter(User.name == username):
        if password == users.password:
            login_response = packet.Packet("login_response", login="True")
        else :
            login_response = packet.Packet("login_response", login="False")
        connection.out_queue.put(login_response)
clientrequests["login"] = login
host_addr = "130.236.76.103"
host_port = 442

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, struct.pack("i",1))
s.bind((host_addr, host_port))
s.setblocking(0)
s.settimeout(0)
s.listen(5)

print "Server igång på %s:%s" % (host_addr, host_port)
while True:
    try:
        acceptor = select.select([s,], [s,], [s,], 0)[0]
        if acceptor:
            newsocket, addr = s.accept()
            client_sockets[newsocket.fileno()] = newsocket
            connections[newsocket.fileno()] = Connection(newsocket, addr)

            print "new connected %s: %s, %s" % (newsocket.fileno(), newsocket, addr)
            print client_sockets

        read_list, write_list, error_list = select.select(
            client_sockets.values(),
            client_sockets.values(),
            client_sockets.values(), 0)
        to_be_removed = []

        for sock in read_list:
            # TODO: fixa in_buffern :p
            # och in_queue
            connection = connections[sock.fileno()]
            print "läsa från %s" % sock.fileno()
            read = sock.recv(1024)
            if read != "":
                connection.in_buffer += read
                can_split = buffrify.split_buffer(connection.in_buffer)
                if can_split is not None:
                    connection.in_buffer = can_split[1]
                    read = can_split[0]
                    pack = packet.Packet.from_net(read)
                    print "laggar till %s=>%s" % (pack.type, str(pack.data))
                    if pack.type in clientrequests:
                        clientrequests[pack.type](connection, pack)
                    for fileno, connection in connections.iteritems():
                        if sock.fileno() != fileno:
                            connection.out_queue.put("%s hälsar: %s" % \
                                    (sock.fileno(), read))
            else:
                to_be_removed.append(sock.fileno())


        for sock in write_list:
            connection = connections[sock.fileno()]

            if connection.out_buffer == "" and \
                not connection.out_queue.empty():
                connection.out_buffer = buffrify.create_pack(str(connection.out_queue.get()))

            if connection.out_buffer != "":
                sent = sock.send(connection.out_buffer)
                if sent != len(connection.out_buffer):
                    connection.out_buffer = connections[sock.fileno()].out_buffer[sent:]
                else:
                    connections[sock.fileno()].out_buffer = ""

        for sock in error_list:
            print "fel på %s" % sock.fileno()

        # logics
        for fileno, connection in connections.iteritems():
            if time.time()-connection.timestamp > connection.pingtime: 
                connection.timestamp = time.time()
                if connection.timepinged == 3:
                    print "You tried to connect to klient:" , connection.socket.fileno() , \
                            "three times you will now remove that client" 
                    connection.timepinged == 0
                    to_be_removed.append(connection.socket.fileno())
                else:
                    connection.timepinged = connection.timepinged + 1
                    ping = packet.Packet("ping")
                    connection.out_queue.put(ping)

        for id in to_be_removed:
            connections[id].socket.close()
            client_sockets[id].close()
            del connections[id]
            del client_sockets[id]

    except KeyboardInterrupt:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        for sock in client_sockets.values():
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
    except socket.error:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        for sock in client_sockets.values():
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
