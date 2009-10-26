import socket
HOST = '192.168.1.49'                 # Symbolic name meaning all available interfaces
PORT = 443              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print 'Server is listening...'
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(10000000)
    if not data: break
    conn.send(data)
conn.close()
