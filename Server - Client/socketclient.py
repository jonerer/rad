# Echo client program
import socket

HOST = '192.168.1.49'    # The remote host
PORT = 443              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
f = open('/home/lytharn/Python/text.txt', 'r')
polentext = f.read()
f.close()
s.send(polentext)
data = s.recv(10000000)
s.close()
print 'Received', repr(data)
f = open('result.txt', 'w')
f.write(repr(data))
f.close()
