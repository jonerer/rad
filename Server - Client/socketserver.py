# -*- coding: utf-8 -*
import socket, threading, sys, Queue
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD, SysCallError

class SocketServer(object):
    """This class is setting up a server that is listining to port 443
    """
    certpath = "ca/cert.pem"
    keypath = "ca/key.pem"
    BUFF = 8192

    def __init__(self, HOST='130.236.219.232', PORT = 443):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = Context(TLSv1_METHOD)
        context.use_certificate_file((self.certpath))
        context.use_privatekey_file(self.keypath)
        context.set_timeout(2)
        conn = Connection(context,s)
        conn.bind((HOST,PORT))

        print 'Server is listening...'
        conn.listen(5)
        # self.client_table is a dictionary of clients
        # where key = unique id and value = socket
        self.client_table = {} 
        self.id_counter = 0
        self.in_q = Queue.Queue()
        self.out_q = Queue.Queue()
        threading.Thread(target=self.sendinput).start()
        threading.Thread(target=self.in_processor).start()
        threading.Thread(target=self.out_processor).start()
        try:
            while True:
        # Waiting for new client to accept, sslsocket is the socket that will be used for communication with this client after a client sets up a connection with the server
                sslsocket, addr = conn.accept()
                self.client_table[self.id_counter] = sslsocket
                self.id_counter = self.id_counter + 1
                threading.Thread(target=self.client_handler,args=(self.id_counter-1,)).start()
        except KeyboardInterrupt:
            for key, value in self.client_table.iteritems():
                value.shutdown()
                value.close()
            sys.exit(0)

    #Handle the clients requests
    def client_handler(self, id):
        sslsocket = self.client_table[id]
        print "Klient: ", str(sslsocket), " ansluten"
        while True:
            output = self.receive(id)
            self.in_q.put((id, output))
        

    def receive(self, id):
        sslsocket = self.client_table[id]
        output = ""
        try:
            data = sslsocket.recv(self.BUFF)
            if data == "start":
                while True:
                    data = sslsocket.recv(self.BUFF)
                    if data == "end":
                        return output
                        output = ""
                        break
                    output = output + data
        except SysCallError:
            print "klient", str(sslsocket), "disconnected"
            print "SysCallError i receive"
            del self.client_table[id]
            sslsocket.shutdown()
            sslsocket.close()

    #Sends a string to a specific socket 
    def send(self, id, str):
        socket = self.client_table[id]
        socket.write("start")
        totalsent =  0
        while totalsent < str.__len__():
            sent = socket.write(str[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent
        socket.write("end")

    #Takes input from the server and sends to all clients
    def sendinput(self):
        while True:
            input = raw_input()
            for id, socket in self.client_table.iteritems():
                self.out_q.put((id, input))

    def in_processor(self):
        while True:
            self.parse(self.in_q.get())

    def parse(self,str):
        print str

    def out_processor(self):
        while True:
            id, data = self.out_q.get()
            self.send(id, data)

SocketServer()
