#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


def readData():
    
    f = open('cars.sql', 'r')
    
    with f:
        data = f.read()
        f.close()
        return data
        

con = lite.connect(':memory:')

with con:   

    cur = con.cursor()
    
    sql = readData()
    cur.executescript(sql)
    
    cur.execute("SELECT * FROM Cars")
    
    rows = cur.fetchall()
    
    for row in rows:
        print row    
con.close()
