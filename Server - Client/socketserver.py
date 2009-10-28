# -*- coding: utf-8 -*
import socket, ssl, threading

class SocketServer(object):

    certpath = "ca/cert.pem"
    keypath = "ca/key.pem"

    def __init__(self, HOST='127.0.1.1', PORT = 443):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        print 'Server is listening...'
        s.listen(5)
        self.socketclienttable = {}
        self.clientid = 0
        while True:
        # Waiting for new client to accept
            conn, addr = s.accept()
            sslsocket = self.wrapsocket(conn,addr)
            self.socketclienttable[self.clientid] = sslsocket
            self.clientid = self.clientid + 1
            threading.Thread(target=self.write,args=(self.clientid-1,)).start()

    def wrapsocket(self, socket,address):
        sslsocket = ssl.wrap_socket(socket, server_side=True, certfile=self.certpath, keyfile=self.keypath, ssl_version=ssl.PROTOCOL_SSLv23)
        print 'Connected by', address
        return sslsocket
    
    def write(self, id):
        socket = self.socketclienttable[id]
        utdata = ""
        while True: 
            data = socket.read(8192)
            if not data: break 
            utdata = utdata + str(data)
        socket.close()
        f = open('Data sent/result' + repr(id) + ".txt", 'w')
        f.write(utdata)
        f.close

socketArray = list()
