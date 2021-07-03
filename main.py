from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SOCK_DGRAM
import time
import sqlite3
import re
from querycontacts import ContactFinder
from ip2geotools.databases.noncommercial import DbIpCity
import atexit

banner = b"""
 _    _                  _             
| |  | |                (_)            
| |  | | __ _ _ __ _ __  _ _ __   __ _ 
| |/\| |/ _` | '__| '_ \| | '_ \ / _` |
\  /\  / (_| | |  | | | | | | | | (_| |
 \/  \/ \__,_|_|  |_| |_|_|_| |_|\__, |
                                  __/ |
                                 |___/ 
THIS IS A DUMMY SERVER TRACKING COMPROMISED HOSTS, CLOSE YOUR CLIENT IMMEDIATELY.
VOILATIONS WILL BE REPORTED TO THE ABUSE CONTACT ASSOCIATED WITH YOUR IP ADDRESS
root@honeypie:~$"""

# Function for long and lat

def geo(ip):

    try:
        response = DbIpCity.get(ip, api_key='free')

        print(response.latitude)
        print(response.longitude)
        return response.latitude, "#", response.longitude

    except:
        return "0", "#", "0"
# Get source ip and port

def ipandport(inf):
    srcipandport = inf.split("raddr",1)[1]
    infip, infprt = srcipandport.split(",")
    infprt = re.sub("[)>]", "", infprt)
    infip = re.sub("[=(']", "", infip)
    return infip, infprt
# Functions for adding to database

def add_entry(uid, srcip, srcport, thetime, abuse, latitude, longitude, user, password, command):
    c.execute('''INSERT INTO information VALUES ("{}","{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}") '''.format(uid, srcip, srcport, thetime, abuse, latitude, longitude, user, password, command))  # insert values
    connsq.commit()


#Create my Database
connsq = sqlite3.connect('conn_data.db')  # actually creates file called student_data.db
c = connsq.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS information (uid text, source IP text, port text, time text, abuse text, latitude text, longitude text, user text, password text, command text) ''')  # add "information" table to database
connsq.commit()

#Listen for connections
sk=socket(AF_INET,SOCK_STREAM)
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind(('0.0.0.0',23))


try:
    testuid = c.execute("SELECT uid FROM information ORDER BY uid DESC LIMIT 1").fetchall()
    uid = int(testuid[0][0])

except:
    uid = 0
#testy = str(testuid[0])
#uidextract = re.findall(r'\d', str(testuid[0]))
#uid = int(uidextract[0])
#uid = 0

while True:
    sk.listen()
    conn,addr = sk.accept()
    conn.settimeout(10)

    constr = str(conn)
# Sanitizing the connection information to place into database (src, prt and abuse)
#TODO: MAKE THIS INTO FUNCTIONS - need a try loop
    srcip, srcprt = ipandport(constr)
    curtime = time.time()
    print(srcip)
    print(srcprt)
    print(time.time())

#getting my abuse email
    try:
        qf = ContactFinder()
        print(qf.find(srcip))
        abuse = qf.find(srcip)
        abuse = abuse[0]

    except:
        abuse = "localip@localipaddress"
        print(abuse)
    # get geo data
    LonLat = geo(srcip)
    latitude = LonLat[0]
    longitude = LonLat[2]




    try:
        conn.send(b"Welcome to the FBI Secret Database\nUsername:")
        hasprovidedusename = 0
        morecommands = 0
        command = ""
        timeout = time.time()

# Extremely hacky attempt at some interaction
        while True:

            data = conn.recv(1024)
            print(data.decode('utf-8', "ignore"))
            print(len(data))

            if morecommands == 1:
                command = command + data.decode('utf-8', "ignore")
                c.execute("""UPDATE information SET command = ? WHERE uid = ?""",
                          (data.decode('utf-8', "ignore") + command, uid))
                connsq.commit()
                conn.send(b"root@honeypie:~$")
                continue


            # set timeout for stuck connections
            if time.time() > timeout + 10:
                conn.close()

            # Here client has provided user and password, see the warning message and tried to run a command
            if hasprovidedusename == 2:
                conn.send(b"root@honeypie:~$")
                # update our database with the connection
                command = command + data.decode('utf-8', "ignore")
                uid = uid +1
                add_entry(uid, srcip, srcprt, curtime, abuse, latitude, longitude, username, password, command)
                morecommands = 1

            # Warning banner sent
            if hasprovidedusename == 1:
                conn.send(banner)
                hasprovidedusename = 2
                password = data.decode('utf-8', "ignore")
                continue
            # Initial connect - need to ignore the data sent
            if len(data) in range(20, 30):
                continue

            # Has provided a username
            if len(data) > 0:
                username = data.decode('utf-8', "ignore")
                conn.send(b"Password:")
                hasprovidedusename = 1
                continue

 #   except BrokenPipeError:
        break

    except:

        conn.close()
        continue
    #except Exception as e:
    #    print(e)