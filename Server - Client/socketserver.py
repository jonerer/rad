import socket, ssl
HOST = '192.168.1.36'                 # Symbolic name meaning all available interfaces
PORT = 443              # Arbitrary non-privileged port
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
#while 1:
#    data = conn.recv(10000000)
#    if not data: break
#    conn.send(data)
# null data means the client is finished with us
while True:
    data = connstream.read()
    if not data: break
    print "Hejsan"
    connstream.write(data) 
# finished with client
connstream.close()
