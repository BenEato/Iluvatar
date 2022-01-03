import sqlite3
import time
import datetime


def emailgen(input):
    y = len(input)
    x = 0
    listofattacksbyabuse = ""
    while x < y:
        normaltime = float(input[x][0])
        normaltime = int(normaltime)
        timestamp = datetime.datetime.fromtimestamp(normaltime)
        tabletime = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        #print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        #print(input[x])
        #print(tabletime + " | " + str(input[x][2]) + " | " + str(input[x][3]))
        listofattacksbyabuse += tabletime + " | " + str(input[x][2]) + " | " + str(input[x][3]) + "\n"
        x += 1
        #print(listofattacksbyabuse)
    return(listofattacksbyabuse)

# get epoch time for yesterday
currenttime = time.time()
# yesterdaytime = currenttime - 86400
yesterdaytime = currenttime - 172800
yesterdaytime = str(yesterdaytime)
print(yesterdaytime)

# open the database
connection = sqlite3.connect("conn_data.db")
cursor = connection.cursor()
# get results from last 24 hours
rows = cursor.execute("SELECT time, abuse, port FROM information WHERE time > " + yesterdaytime + " GROUP BY abuse").fetchall()

# Create a list of unique abuse emails for us to work through
x = 0
abuselist = []
while True:
    try:
        #print(rows[x][1])
        abuselist.append(rows[x][1])
        x += 1
        #print(abuselist)
    except:
        break

print("listdone")
print(len(abuselist))

# SELECT time, abuse, port FROM information WHERE time > 1624535103 AND abuse LIKE '%aussie%'

# for loop through unique abuse email and return all attacks associated with it
for i in abuselist:
    print(i)
    attackexamples = cursor.execute("SELECT time, abuse, source, port FROM information WHERE time > 1624535103 AND abuse LIKE '%" + i + "%'").fetchall()
    # consider using tabulate here
    emailgen(attackexamples)
    print("""Hello, \n
The following IP addresses have been detected attempting to access honeypot
at IPADDRESS \n
    TIME       | SOURCE IP | PORT \n""" + str(emailgen(attackexamples)))