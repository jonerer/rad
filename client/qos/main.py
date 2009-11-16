# -*- coding: utf-8 -*
# Echo client program
import socket, sys, time, select, time
# require a certificate from the server
import Queue
import threading
import gtk
from shared import rpc, buffrify, packet
from simplejson import loads, dumps

rpc.set_name("qos")

if "--no-connect" in sys.argv:
    no_connect = True

network_listeners = {}

def read_keys():
    global connection
    while connection.connected:
        input = raw_input()
        connection.out_queue.put(packet.Packet("chat",
            message=input))

class Connection(object):

    #The time the client need to hear from     
    
    def __init__(self):
        self.pingtime = 6
        self.host_addr = "130.236.76.135"
        #self.host_addr = "localhost"
        self.host_port = 442
        
        self.out_queue = Queue.Queue()
        self.out_buffer = ""
        
        self.in_buffer = ""

        self.KeyboardInterrupt = False
        self.connected = False
        self.reconnect()


    def reconnect(self):
        print "Du kör reconnect"
        while not self.connected and not self.KeyboardInterrupt:
            print "Du är inne i while"
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print self.s.connect((self.host_addr, self.host_port))
                self.connected = True
                print "har kontakt med %s:%s" % (self.host_addr, self.host_port)
                self.timestamp = time.time()
            except socket.error:
                time.sleep(5)
                print "Couldn't connect to that server"
            if self.connected:
                threading.Thread(target=self.send).start()
                self.receive()
                break

    def receive(self):
        while self.connected:
            try:
                read = self.s.recv(1024)
                if read != "":
                    self.in_buffer += read
                    can_split = buffrify.split_buffer(self.in_buffer)
                    if can_split is not None:
                        self.in_buffer = can_split[1]
                        print "> %s" % can_split[0]
                        pack = packet.Packet.from_net(can_split[0])
                        if pack.type in network_listeners:
                            print "fanns en som lyssna på %s" % pack.type
                            network_listeners[pack.type](pack)
                else:
                    self.connected = False
                    print "fick en tom read i client"
                    break
            except KeyboardInterrupt:
                self.KeyboardInterrupt = True
                print "fick interrupt i receive"
                self.connected = False

    def add_packet(self, packet):
        """ receives stuff from dbus and DOO EEETT"""
        self.out_queue.put(packet)

    def send(self):
        while self.connected:
            if self.out_buffer == "":
                try:
                    new_out_buffer = self.out_queue.get(True, 1)
                        # blocks for a while
                    self.out_buffer = buffrify.create_pack(str(new_out_buffer))
                except Queue.Empty:
                    pass
            if self.out_buffer != "":
                sent = self.s.send(self.out_buffer)
                if sent != len(self.out_buffer):
                    print "lyckades inte tömma hela"
                    self.out_buffer = self.out_buffer[sent:]
                else:
                    self.out_buffer = ""
            if time.time()-self.timestamp > self.pingtime:
                print "server has gone down bad"
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.connected = False
        print "Du har stängt av allt i socketen"
        try:
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
        except socket.error:
            print "Socket är redan stängd"
        if not self.KeyboardInterrupt:
            self.reconnect()

connection = Connection()
if "--read-keys" in sys.argv or True: # ha true nu iaf 
    threading.Thread(target=read_keys).start()

def ping_response(packet):
    global connection
    print "ska svara på pingz"... men fuck it
    connection.timestamp = time.time()
    connection.out_queue.put(packet.Packet("pong"))
network_listeners["ping"] = ping_response

def request_login(username, password):
    connection.add_packet(dumps({"action": "login", 
        "username": username, 
        "password": password}))

rpc.register("request_login", request_login)
rpc.register("add_packet", connection.add_packet)

