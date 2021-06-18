from socket import socket, AF_INET, SOCK_STREAM
import time
sk=socket(AF_INET,SOCK_STREAM)
sk.bind(('192.168.1.110',34))
sk.listen()
conn,addr = sk.accept()
conn.sendall(b"Welcome to FBI Secret Database\n username:")
constr = str(conn)
print(constr.split("raddr",1)[1])
print(time.gmtime())
while True:
    data = conn.recv(1024)
    print(data.decode())