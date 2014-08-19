# -*- coding: utf-8 -*-
import urllib2
import json
import re
import time
import sqlite3
transportList = urllib2.urlopen('http://transit.in.ua/').read().decode('utf-8')
busList = frozenset(re.findall(r'(dnepropetrovsk-taxi-\d+A?)',transportList, re.MULTILINE))
attrs = ("&".join(["dataRequest[]=" + i for i in list(busList)]))

# Create table
conn = sqlite3.connect('bus.db')
c = conn.cursor()
#c.execute('''CREATE TABLE logs (
#	id integer primary key, 
#	title text, 
#	longitude real, 
#	latitude real, 
#	angle real, 
#        bus_id integer,
#        velocity real,
#	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#);''')
conn.commit()
conn.close()
while True:
	conn = sqlite3.connect('bus.db')
	c = conn.cursor()
        try:
            busRequest = urllib2.urlopen(
                "http://transit.in.ua/importTransport.php?" +
                attrs).read()
            positionData = json.loads(busRequest.decode('utf-8'))
        except:
            continue

        countBuses = {}
        for item in positionData:
	    print item
	    c.execute('''INSERT INTO logs (
                title, 
                longitude, 
                latitude, 
                bus_id,
                velocity,
                angle) VALUES (?,?,?,?,?,?)''', (
                item["info"], 
                item["cordinate"][0], 
                item["cordinate"][1], 
                item["id"], 
                item["velocity"], 
                item["angle"]
        ))
	conn.commit()
	conn.close()
        time.sleep(60)
