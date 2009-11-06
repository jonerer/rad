# -*- coding: utf-8 -*
# Echo client program
import socket, sys, time, select, time
# require a certificate from the server
from Queue import Queue
import threading
import gtk
from shared import rpc
from simplejson import loads, dumps

rpc.set_name("qos")

if "--no-connect" in sys.argv:
    no_connect = True

def read_keys():
    while True:
        global connection
        input = raw_input()
        connection.out_queue.put(input)

class Connection(object):
    def __init__(self):
        self.host_addr = "130.236.219.121"
        #self.host_addr = "localhost"
        self.host_port = 442

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host_addr, self.host_port))

        self.out_queue = Queue()
        self.out_buffer = ""

        threading.Thread(target=self.send).start()

    def receive(self):
        while True:
            read = self.s.recv(1024)
            if read != "":
                print "> %s" % read

    def add_packet(self, packet):
        """ receives stuff from dbus and DOO EEETT"""
        self.out_queue.put(packet)

    def send(self):
        while True:
            if self.out_buffer == "":
                self.out_buffer = self.out_queue.get() # blocks

            sent = self.s.send(self.out_buffer)
            if sent != len(self.out_buffer):
                print "lyckades inte tömma hela"
                self.out_buffer = self.out_buffer[sent:]
            else:
                self.out_buffer = ""


connection = Connection()
if "--read-keys" in sys.argv or True: # ha true nu iaf
    threading.Thread(target=read_keys).start()

def request_login(username, password):
    connection.add_packet(dumps({"action": "login", 
        "username": username, 
        "password": password}))

rpc.register("request_login", request_login)
rpc.register("add_packet", connection.add_packet)

connection.receive()
