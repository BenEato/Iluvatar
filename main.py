import socket
import re
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
import time
sk=socket(AF_INET,SOCK_STREAM)
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('192.168.1.110',23))
while True:
    sk.listen()
    conn,addr = sk.accept()

    conn.sendall(b"Welcome to FBI Secret Database\n username:")
    constr = str(conn)
    print(constr.split("raddr",1)[1])
    srcipandport = constr.split("raddr",1)[1]
    srcip, srcprt = srcipandport.split(",")
    srcprt = re.sub("[)>]", "", srcprt)
    srcip = re.sub("[=(']", "", srcip)
    print(srcip)
    print(srcprt)
    print(time.localtime())
    while True:
        data = conn.recv(1024)
        try:
            print(data.decode())

        except UnicodeDecodeError:
            conn.close()
            break