from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SOCK_DGRAM
import time
import sqlite3
import re
from querycontacts import ContactFinder
from ip2geotools.databases.noncommercial import DbIpCity
import atexit


# Function for long and lat

def geo(ip):
    #handle private ip for testing
    if "192.168" in ip:
        return "0", "#", "0"
    else:
        response = DbIpCity.get(ip, api_key='free')

        print(response.latitude)
        print(response.longitude)
        return response.latitude, "#", response.longitude

# Get source ip and port

def ipandport(inf):
    srcipandport = inf.split("raddr",1)[1]
    infip, infprt = srcipandport.split(",")
    infprt = re.sub("[)>]", "", infprt)
    infip = re.sub("[=(']", "", infip)
    return infip, infprt
# Functions for adding to database

def add_entry(srcip, srcport, thetime, abuse, latitude, longitude):
    c.execute('''INSERT INTO information VALUES ("{}", "{}", "{}", "{}", "{}", "{}") '''.format(srcip, srcport, thetime, abuse, latitude, longitude))  # insert values
    connsq.commit()


#Create my Database
connsq = sqlite3.connect('conn_data.db')  # actually creates file called student_data.db
c = connsq.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS information (source IP text, port text, time text, abuse text, latitude text, longitude text) ''')  # add "information" table to database
connsq.commit()

#Listen for connections
sk=socket(AF_INET,SOCK_STREAM)
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('0.0.0.0',23))

while True:
    sk.listen()
    conn,addr = sk.accept()
    conn.settimeout(10)

    constr = str(conn)
# Sanitizing the connection information to place into database (src, prt and abuse)
#TODO: MAKE THIS INTO FUNCTIONS
    srcip, srcprt = ipandport(constr)
    curtime = time.time()
    print(srcip)
    print(srcprt)
    print(time.time())

#getting my abuse email
    qf = ContactFinder()
    print(qf.find(srcip))
    abuse = qf.find(srcip)
    abuse = abuse[0]

    # get geo data
    LonLat = geo(srcip)
    latitude = LonLat[0]
    longitude = LonLat[2]


    #update our database with the connection
    add_entry(srcip, srcprt, curtime, abuse, latitude, longitude)

    try:
        conn.send(b"Welcome to the FBI Secret Database\nUsername:")
        hasprovidedusename = 0
        timeout = time.time()
# Extremely hacky attempt at some interaction
        while True:

            data = conn.recv(1024)
            print(data.decode('utf-8', "ignore"))
            print(len(data))

            # set timeout for stuck connections

            print(time.time())
            print(timeout)

            if time.time() > timeout + 10:
                conn.close()

            if hasprovidedusename == 2:
                conn.send(b"root@honeypie:~$")

                continue
            if hasprovidedusename == 1:
                conn.send(b"Welcome to the honeypot!:\nroot@honeypie:~$")
                hasprovidedusename = 2
                continue

            if len(data) in range(20, 30):
                continue

          #  if len(data) == 27:
           #     continue

            if len(data) > 0:
                conn.send(b"Password:")
                hasprovidedusename = 1
                continue

 #   except BrokenPipeError:
        break

    except:
        conn.close()
        continue
