# -*- coding: utf-8 -*
# Echo client program
import socket, sys, time, select, time
# require a certificate from the server
from Queue import Queue
import threading

#HOST = "130.236.219.232"
HOST = "localhost"
PORT = 443

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(0)

# TODO: fixa in-buffer o in-kö

out_queue = Queue()
out_buffer = ""

def read_keys():
    while True:
        input = raw_input()
        out_queue.put(input)

threading.Thread(target=read_keys).start()

while True:
    read_list, write_list, xlist = select.select([s,], [s,], [s,], 0)

    if read_list:
        read = s.recv(1024)
        if read != "":
            print read

    if write_list:
        if out_queue.qsize() != 0:
            print "nurå"
        if out_buffer == "" and not out_queue.empty():
            out_buffer = out_queue.get()

        if out_buffer != "":
            print "här ska skrivas! %s" % out_buffer
            sent = s.send(out_buffer)
            if sent != len(out_buffer):
                print "lyckades inte tömma hela buffern."
                out_buffer = out_buffer[sent:]
            else:
                out_buffer = ""
    
