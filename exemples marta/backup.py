#Creating a Backup of BD

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

cars = (
    (1, 'Audi', 52643),
    (2, 'Mercedes', 57642),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
)

def writeData(data):
    
    f = open('cars.sql', 'w')
    
    with f:
        f.write(data)

    f.close()


con = lite.connect(':memory:')

with con:
    
    cur = con.cursor()
    
    cur.execute("DROP TABLE IF EXISTS Cars")
    cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
    cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
    cur.execute("DELETE FROM Cars WHERE Price < 30000")
    
    data = '\n'.join(con.iterdump())
    
    writeData(data)
con.close()
