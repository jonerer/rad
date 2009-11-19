# -*- coding: utf-8 -*
# Echo client program
import socket, sys, time, select
# require a certificate from the server
import Queue
import threading
import gtk
from shared import rpc, buffrify
from shared.packet import Packet
from simplejson import loads, dumps
import subprocess
subprocess.call('ssh -f jonas@130.236.76.103 -L 442:127.0.0.1:442 -N sleep 1',shell=True)


import subprocess^M
subprocess.call('ssh -f jonas@130.236.76.103 -L 442:127.0.0.1:442 -N sleep 1',shell=True)

rpc.set_name("qos")

if "--no-connect" in sys.argv:
    no_connect = True

network_listeners = {}

def read_keys():
    global connection
    while connection.connected:
        input = raw_input()
        connection.out_queue.put(Packet("chat",
            message=input))


class Connection(object):

    #The time the client need to hear from     
    
    def __init__(self):
        self.pingtime = 6
        self.host_addr = "130.236.189.23"
        #self.host_addr = "localhost"
        self.host_port = 2345
        
        self.out_queue = Queue.Queue()
        self.out_buffer = ""
        
        self.in_buffer = ""

        self.KeyboardInterrupt = False
        self.connected = False

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
                        pack = Packet.from_str(can_split[0])
                        print "> %s, %s" % (pack.type, str(pack.data))
                        if pack.type in network_listeners:
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
        loginpacket = Packet.from_str(packet)
        self.out_queue.put(loginpacket)

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

def ping_response(pack):
    connection.timestamp = time.time()
    connection.out_queue.put(Packet("pong"))
network_listeners["ping"] = ping_response

def login_response(pack):
    login_boolean = parseBoolean(pack.data["login"])
    connection.timestamp = time.time()
    if login_boolean:
        rpc.send("main", "access", bol=login_boolean)
    if not login_boolean:
        rpc.send("main", "access", bol=login_boolean)
network_listeners["login_response"] = login_response

def parseBoolean(login):
    return login == "True"

def alarm_response(pack):
    print pack.data
network_listeners["alarm_response"] = alarm_response
    

rpc.register("add_packet", connection.add_packet)
threading.Thread(target=connection.reconnect).start()
gtk.gdk.threads_init()
gtk.main()
