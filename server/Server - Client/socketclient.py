# -*- coding: utf-8 -*
# Echo client program
import socket, threading, sys, time # require a certificate from the server
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD
from OpenSSL import SSL

#varför vill inte tråden "sendinput" lyssna på keyboardinterrupt?

class SocketClient(object):
    """This class sends all info to the server
    """

    cacertpath = "ca/cacert.pem"
    BUFF = 8192

    def __init__(self,HOST='130.236.219.232', PORT = 443):
        self.mutex = threading.Semaphore(1)
        self.connected = False
        self.connect()
        self.host_addr = HOST
        self.host_port = PORT

    def connect(self):
        print "You are trying to connect..."
        for x in range(7):
            if not self.connected:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    context = Context(TLSv1_METHOD)
                    context.use_certificate_file(self.cacertpath)
                    context.set_timeout(2)
                    self.sslsocket = Connection(context,s)
                    self.sslsocket.connect((self.host_addr,self.host_port))
                    #starting a thread that listen to what server sends which the clients need to be able to send and recive data at the same time
                    t = threading.Thread(target=self.receive)
                    t.daemon = True
                    t.start()
                    if self.sslsocket:
                        self.connected = True
                    print "connection established"
                    #self.authentication("Kalle", "te")
                    t = threading.Thread(target=self.sendinput)
                    t.start()
                except socket.error:
                    print "You failed to connect, retrying......."
                    time.sleep(5)

    def authentication(self, username, password):
        self.sslsocket.send(username)
        self.sslsocket.send(password)

    #sending string to server
    def send(self,str):
        try:
            self.sslsocket.write("start")
            totalsent =  0
            while totalsent < str.__len__():
                sent = self.sslsocket.write(str[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
            self.sslsocket.write("end")
        except SSL.SysCallError:
            print "your server is dead, you have to resend data"
            self.connected = False
            self.sslsocket.shutdown()
            self.sslsocket.close()
            self.mutex.acquire()
            print "Du är inne i connect via send SysCallError"
            self.connect()
            self.mutex.release()
        except SSL.Error:
            self.connected = False
            self.mutex.acquire()
            print "Du är inne i connect via send ssl error"
            self.connect()
            self.mutex.release()

    #Sending input to server
    def sendinput(self):
        try:
            while True:
                input = raw_input()
                self.send(input)
        except KeyboardInterrupt:
            print "du är inne i sendinput"
            self.sslsocket.shutdown()
            self.sslsocket.close()
            exit(0)

    #getting data from server
    def receive(self):
        output = ""
        try:
            while True:
                data = self.sslsocket.recv(self.BUFF)
                if data == "start":
                    while True: 
                        data = self.sslsocket.recv(self.BUFF)
                        if data == "end":
                            print output
                            output = ""
                            break
                        output = output + data
        except SSL.SysCallError:
            print "OMG Server is down"
            self.connected = False
            print self.connected
            self.sslsocket.shutdown()
            self.sslsocket.close() 
            self.mutex.acquire()
            self.connect()
            self.mutex.release()

SocketClient()
