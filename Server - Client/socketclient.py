# Echo client program
import socket, ssl, pprint# require a certificate from the server

HOST = '192.168.1.36'    # The remote host
PORT = 443              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="ca/cacert.pem",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect((HOST, PORT))

#s.connect((HOST, PORT))
f = open('text.txt', 'r')
polentext = f.read()
f.close()
print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())
ssl_sock.write(polentext)
#s.send(polentext)
print "2"
data = ssl_sock.read()
#s.recv(10000000)
print "1"
ssl_sock.close()
print 'Received', repr(data)
f = open('result.txt', 'w')
f.write(repr(data))
f.close()
