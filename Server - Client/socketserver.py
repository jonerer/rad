# -*- coding: utf-8 -*
import socket, threading
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD

class SocketServer(object):
    """This class is setting up a server that is listining to port 443
    """
    certpath = "ca/cert.pem"
    keypath = "ca/key.pem"
    BUFF = 8192

    def __init__(self, HOST='127.0.1.1', PORT = 443):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = Context(TLSv1_METHOD)
        context.use_certificate_file((self.certpath))
        context.use_privatekey_file(self.keypath) 
        conn = Connection(context,s)
        conn.bind((HOST,PORT))
        print 'Server is listening...'
        conn.listen(5)
        self.socketclienttable = {}
        self.clientid = 0
        while True:
        # Waiting for new client to accept
            sslsocket, addr = conn.accept()
            print 'Connected to', addr
            self.socketclienttable[self.clientid] = sslsocket
            self.clientid = self.clientid + 1
            threading.Thread(target=self.receive,args=(self.clientid-1,)).start()
            while True:
                    hejsan = self.sendinput()
                    self.send(sslsocket,hejsan)

    def receive(self, id):
        sslsocket = self.socketclienttable[id]
        output = ""
        try: 
            while True:
                data = sslsocket.recv(self.BUFF)
                if data == "start":
                    while True:
                        data = sslsocket.recv(self.BUFF)
                        if data == "end":
                            if output == "hejsan":
                                print "lol"
                                #hejsan = self.sendinput()
                                self.send(sslsocket,"hejsan") 
                                #threading.Thread(target=self.send,args=((sslsocket, "hi client"))).start()
                            print output
                            output = ""
                            break
                        output = output + data
        except KeyboardInterrupt:
            sslsocket.close()
            exit()

    def send(self, socket, str):
        socket.write("start")
        totalsent =  0
        while totalsent < str.__len__():
            sent = socket.write(str[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent
        socket.write("end")

    
    def sendinput(self):
        input = raw_input()
        return input

tjabba = SocketServer()
