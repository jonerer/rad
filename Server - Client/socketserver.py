import socket, ssl
HOST = '127.0.1.1' # Symbolic name meaning all available interfaces
PORT = 443 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print HOST
print PORT
s.bind((HOST, PORT))
print 'Server is listening...'
s.listen(1)
conn, addr = s.accept()
connstream = ssl.wrap_socket(conn, 
                                server_side=True,
                                certfile="ca/cert.pem",
                                keyfile="ca/key.pem",
                                ssl_version=ssl.PROTOCOL_SSLv23)
print 'Connected by', addr
print socket.gethostbyname(socket.gethostname())
utdata = ""
while True: 
    data = connstream.read(8192)
    if not data: break 
    utdata = utdata + str(data)
print "Servern har denna utdata", utdata
connstream.close()
f = open('result.txt', 'w')
f.write(utdata)
f.close