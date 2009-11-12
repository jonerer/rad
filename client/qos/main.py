# -*- coding: utf-8 -*
# Echo client program
import socket, sys, time, select, time
# require a certificate from the server
import Queue
import threading
import gtk
from shared import rpc
from simplejson import loads, dumps

rpc.set_name("qos")

if "--no-connect" in sys.argv:
    no_connect = True

def read_keys():
    global connection
    while connection.connected:
        input = raw_input()
        connection.out_queue.put(input)

class Connection(object):

    #The time the client need to hear from     
    
    def __init__(self):
        self.pingtime = 6
        self.host_addr = "130.236.217.83"
        #self.host_addr = "localhost"
        self.host_port = 442
        
        self.out_queue = Queue.Queue()
        self.out_buffer = ""
        
        self.KeyboardInterrupt = False
        self.connected = False
        self.reconnect()

    def reconnect(self):
        print "Du kör reconnect"
        while not self.connected and not self.KeyboardInterrupt:
            print "Du är inne i while"
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host_addr, self.host_port))
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
                    print "> %s" % read
                    if read == "ping":
                        self.timestamp = time.time()
                        self.out_queue.put("pong")
                if read == "":
                    self.connected = False
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
                    self.out_buffer = new_out_buffer
                except Queue.Empty:
                    print "tom kö ju :o kör ja igen? %s" % self.connected
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

def request_login(username, password):
    connection.add_packet(dumps({"action": "login", 
        "username": username, 
        "password": password}))

rpc.register("request_login", request_login)
rpc.register("add_packet", connection.add_packet)

