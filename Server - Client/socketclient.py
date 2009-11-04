# -*- coding: utf-8 -*
# Echo client program
import socket, threading # require a certificate from the server
from OpenSSL.SSL import Context, Connection, TLSv1_METHOD

class SocketClient(object):
    """This class talks to the server
    """

    cacertpath = "ca/cacert.pem"
    BUFF = 8192

    def __init__(self,HOST='localhost', PORT = 443):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = Context(TLSv1_METHOD)
        context.use_certificate_file(self.cacertpath)
        context.set_timeout(2)
        self.sslsocket = Connection(context,s)
        self.sslsocket.connect((HOST,PORT))
        #starting a thread that listen to what server sends which the clients need to be able to send and recive data at the same time
        self.connection_killed = False
        threading.Thread(target=self.receive).start()
        print "Yeah, tråden fungerar"
        target=self.sendinput()
    
    #sending string to server
    def send(self,str):
        self.sslsocket.write("start")
        totalsent =  0
        while totalsent < str.__len__():
            sent = self.sslsocket.write(str[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent
        self.sslsocket.write("end")
    
    #Sending input to server
    def sendinput(self):
        try:
            while True:
                input = raw_input()
                self.send(input)
        except KeyboardInterrupt:
            print "fuck this shit"
            self.sslsocket.write("fuckthisshit")
            self.connection_killed = True

    #getting data from server
    def receive(self):
        output = ""
        print "Du är i receive"
        buff = ""
        while not self.connection_killed:
            data = self.sslsocket.recv(self.BUFF)
            buff = data
            if buff == "fuckthisshit":
                self.sslsocket.close()
                break
            if data == "fuckthisshitservergoingdown":
                self.sslsocket.write("fuckthisshit")
                self.sslsocket.close()
                break
            print data
            if data == "start":
                while not self.connection_killed:
                    print "tjock?"
                    data = self.sslsocket.recv(self.BUFF)
                    print "nah, det släppte"
                    if data == "end":
                        print output
                        output = ""
                        break
                    output = output + data

client = SocketClient()
