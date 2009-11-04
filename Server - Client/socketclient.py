# -*- coding: utf-8 -*
# Echo client program
import socket, threading, sys, time # require a certificate from the server
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD, SysCallError

class SocketClient(object):
    """This class sends all info to the server
    """

    cacertpath = "ca/cacert.pem"
    BUFF = 8192
    socketactive = False

    def __init__(self,HOST='localhost', PORT = 443):
        for x in range(7):
            if self.socketactive == False:
                self.reconnect()
                time.sleep(10)

    def reconnect(self,HOST='localhost', PORT = 443):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = Context(TLSv1_METHOD)
            context.use_certificate_file(self.cacertpath)
            context.set_timeout(2)
            self.sslsocket = Connection(context,s)
            self.sslsocket.connect((HOST,PORT))
            #starting a thread that listen to what server sends which the clients need to be able to send and recive data at the same time
            threading.Thread(target=self.receive).start()
            target=self.sendinput()
            self.socketactive = True
        except socket.error:
            print "You failed to connect retrying......."

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
        except SysCallError:
            print "your server is dead, you have to resend data"
            self.socketactive = False
            self.sslsocket.close()
            for x in range(7):
                self.reconnect()
                time.sleep(10)
    
    #Sending input to server
    def sendinput(self):
        try:
            while True:
                input = raw_input()
                self.send(input)
        except KeyboardInterrupt:
            self.sslsocket.close()
            sys.exit(0)

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
        except SysCallError:
            print "OMG Server is down"
            self.sslsocket.shutdown()
            self.sslsocket.close() 
            self.socketactive = False

client = SocketClient()
