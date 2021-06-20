import socket
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
import datetime
import sqlite3
import re

# Functions for adding to database

def add_entry(srcip, srcport, thetime):
    c.execute('''INSERT INTO information VALUES ("{}", "{}", "{}") '''.format(srcip, srcport, thetime))  # insert values
    connsq.commit()


#Create my Database
connsq = sqlite3.connect('conn_data.db')  # actually creates file called student_data.db
c = connsq.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS information (source IP text, port text, time text) ''')  # add "information" table to database
connsq.commit()

#Listen for connections
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
    curtime = datetime.datetime.now()
    print(srcip)
    print(srcprt)
    print(datetime.datetime.now())


    #update our database with the connection
    add_entry(srcip, srcprt, curtime)

    while True:
        data = conn.recv(1024)
        try:
            print(data.decode())

        except UnicodeDecodeError:
            print('Compatibility error')


        #except UnicodeDecodeError:
        except KeyboardInterrupt:
            conn.close()
            break