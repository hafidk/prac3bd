#Metadata of a DB
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

print "Example 1------------------"

con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    
    cur.execute('PRAGMA table_info(Cars)')
    
    data = cur.fetchall()
    
    for d in data:
        print d[0], d[1], d[2]
con.close()

print "Example 2------------------"

#Info about columns of a table
con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    cur.execute('SELECT * FROM Cars')
    
    col_names = [cn[0] for cn in cur.description]
    
    rows = cur.fetchall()
    
    print "%s %-10s %s" % (col_names[0], col_names[1], col_names[2])

    for row in rows:    
        print "%2s %-10s %s" % row
con.close()

print "Example 3 ------------------"

#Print all the tables of the database

con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    rows = cur.fetchall()

    for row in rows:
        print row[0]
con.close()
