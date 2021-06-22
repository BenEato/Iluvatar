from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SOCK_DGRAM
import datetime
import sqlite3
import re
from querycontacts import ContactFinder
import atexit

sk=socket(AF_INET,SOCK_STREAM)
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('192.168.1.110',24))



# Functions for adding to database

def add_entry(srcip, srcport, thetime, abuse):
    c.execute('''INSERT INTO information VALUES ("{}", "{}", "{}", "{}") '''.format(srcip, srcport, thetime, abuse))  # insert values
    connsq.commit()


#Create my Database
connsq = sqlite3.connect('conn_data.db')  # actually creates file called student_data.db
c = connsq.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS information (source IP text, port text, time text, abuse text) ''')  # add "information" table to database
connsq.commit()

#Listen for connections
sk=socket(AF_INET,SOCK_STREAM)
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('192.168.1.110',23))

while True:
    sk.listen()
    conn,addr = sk.accept()
    conn.settimeout(10)

    constr = str(conn)
# Sanitizing the connection information to place into database
    print(constr.split("raddr",1)[1])
    srcipandport = constr.split("raddr",1)[1]
    srcip, srcprt = srcipandport.split(",")
    srcprt = re.sub("[)>]", "", srcprt)
    srcip = re.sub("[=(']", "", srcip)
    curtime = datetime.datetime.now()
    print(srcip)
    print(srcprt)
    print(datetime.datetime.now())
    qf = ContactFinder()
    print(qf.find(srcip))
    abuse = qf.find(srcip)
    abuse = abuse[0]


    #update our database with the connection
    add_entry(srcip, srcprt, curtime, abuse)
    while True:

        try:
            conn.send(b"Welcome to FBI Secret Database\n username:")
            data = conn.recv(1024)
            print(data.decode('utf-8', "ignore"))

        except BrokenPipeError:
            break

        except:
            print("timed out")
            break
