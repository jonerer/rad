# Echo client program
import socket, ssl, pprint # require a certificate from the server
HOST = '127.0.1.1'    # The remote host
PORT = 443              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="ca/cacert.pem",
                           cert_reqs=ssl.CERT_REQUIRED)
ssl_sock.connect((HOST, PORT))
f = open('text.txt', 'r')
polentext = f.read()
f.close()
print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())
totalsent =  0
while totalsent < polentext.__len__():
    sent = ssl_sock.write(polentext[totalsent:totalsent + 1000])
    if sent == 0:
        raise RuntimeError, "socket connection broken"
    totalsent = totalsent + sent
ssl_sock.close()
#print 'Received', repr(data)
#f = open('result.txt', 'w')
#f.write(repr(data))
#f.close()
