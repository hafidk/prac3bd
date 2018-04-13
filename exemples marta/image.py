#!/usr/bin/python
# -*- coding: utf-8 -*-
#Working with images

import sqlite3 as lite
import sys

#Store image in DataBase (BLOB: Binary Large Objects)
def readImage():

    try:
        fin = open("computer.jpg", "rb")
        img = fin.read()
        return img
        
    except IOError, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        
        if fin:
            fin.close()

def writeImage(data):
    
    try:
        fout = open('computer2.jpg','wb')
        fout.write(data)
    
    except IOError, e:    
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
        
    finally:
        
        if fout:
            fout.close()  


try:
    con = lite.connect('test.db')
  
    cur = con.cursor()
    cur.execute("CREATE TABLE Images(Id INTEGER PRIMARY KEY, Data BLOB);")
    data = readImage()
    binary = lite.Binary(data)
    cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,) )

    con.commit()    
    
except lite.Error, e:
    
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()  

#Read Image from Database
   
    

try:
    con = lite.connect('test.db')
    
    cur = con.cursor()    
   
    cur.execute("SELECT Data FROM Images LIMIT 1")
    data = cur.fetchone()[0]
    
    writeImage(data)

    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()      
