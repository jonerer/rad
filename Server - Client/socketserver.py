# -*- coding: utf-8 -*
import socket, threading, sys
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD, SysCallError

class SocketServer(object):
    """This class is setting up a server that is listining to port 443
    """
    certpath = "ca/cert.pem"
    keypath = "ca/key.pem"
    BUFF = 8192

    def __init__(self, HOST='localhost', PORT = 443):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = Context(TLSv1_METHOD)
        context.use_certificate_file((self.certpath))
        context.use_privatekey_file(self.keypath)
        context.set_timeout(2)
        conn = Connection(context,s)
        conn.bind((HOST,PORT))
        print 'Server is listening...'
        conn.listen(5)
        #self.socketclienttable is a dictionary of clients, where each client have an unique id, self.clientid
        self.socketclienttable = {} 
        self.clientid = 0
        threading.Thread(target=self.sendinput).start()
        while True:
        # Waiting for new client to accept, sslsocket is the socket that will be used for communication with this client after a client sets up a connection with the server
            sslsocket, addr = conn.accept()
            self.socketclienttable[self.clientid] = sslsocket
            self.clientid = self.clientid + 1
            threading.Thread(target=self.receive,args=(self.clientid-1,)).start()

    #Handle the clients requests
    def receive(self, id):
        sslsocket = self.socketclienttable[id]
        output = ""
        try:
            while True:
                data = sslsocket.recv(self.BUFF)
                print str(data)
                if data == "fuckthisshit":
                    sslsocket.write("fuckthisshit")
                    sslsocket.close()
                    del self.socketclienttable[id]
                    break
                if data == "start":
                    while True:
                        data = sslsocket.recv(self.BUFF)
                        if data == "end":
                            print output
                            output = ""
                            break
                        output = output + data
        except SysCallError:
            del self.socketclienttable[id]
            sslsocket.close()

    #sends a string to a specific client 
    def send(self, socket, str):
        try:
            socket.write("start")
            totalsent =  0
            while totalsent < str.__len__():
                sent = socket.write(str[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
            socket.write("end")
        except SysCallError:
            self.socketclienttable.remove(socket)
            socket.close()

    #Takes input from the server and sends to all clients
    def sendinput(self):
        try:
            while True:
                input = raw_input()
                for key, value in self.socketclienttable.iteritems():
                    print value
                    self.send(value, input)
            return input
        except KeyboardInterrupt:
            for key, value in self.socketclienttable.iteritems():
                    self.send(value, "fuckthisshitservergoingdown")

server = SocketServer()
