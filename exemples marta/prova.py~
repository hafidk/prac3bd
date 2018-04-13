#!/usr/bin/python
# -*- coding: utf-8 -*-

#Creacio simple de taules, consulta, consultes parametritzades, modificacio de valors

import sqlite3 as lite
import sys

try:
    con = lite.connect('test.db')

    cur = con.cursor()  

    cur.executescript("""
        DROP TABLE IF EXISTS Cars;
        CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
        INSERT INTO Cars VALUES(1,'Audi',52642);
        INSERT INTO Cars VALUES(2,'Mercedes',57127);
        INSERT INTO Cars VALUES(3,'Skoda',9000);
        INSERT INTO Cars VALUES(4,'Volvo',29000);
        INSERT INTO Cars VALUES(5,'Bentley',350000);
        INSERT INTO Cars VALUES(6,'Citroen',21000);
        INSERT INTO Cars VALUES(7,'Hummer',41400);
        INSERT INTO Cars VALUES(8,'Volkswagen',21600);
        """)

    con.commit()
    
except lite.Error, e:
    
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 


#Cursor access. Default: Tuple of tuples

print "Access 1--------"

con = lite.connect('test.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Cars")

    rows = cur.fetchall()

    for row in rows:
        print row
con.close()
#Better access

print "Access 2 ---------------"
con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Cars")

    while True:
      
        row = cur.fetchone()
        
        if row == None:
            break
            
        print row[0], row[1], row[2]
con.close()
#Better access: Dictionary cursor

print "Access 3 ------------------"


con = lite.connect('test.db')    

with con:
    
    con.row_factory = lite.Row
       
    cur = con.cursor() 
    cur.execute("SELECT * FROM Cars")

    rows = cur.fetchall()

    for row in rows:
        print "%s %s %s" % (row["Id"], row["Name"], row["Price"])
con.close()

#Parameterized queries

con = lite.connect('test.db')
print "Parameterized query"

uId=input("Enter id to modify price: ")
uPrice=input("Enter new price: ")

with con:

    cur = con.cursor()    

    cur.execute("UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))        
    con.commit()
    
    print "Number of rows updated: %d" % cur.rowcount
con.close()

#Another parametized query

uId = input("Enter id to query: ")

con = lite.connect('test.db')

with con:

    cur = con.cursor()    

    cur.execute("SELECT Name, Price FROM Cars WHERE Id=:Id", 
        {"Id": uId})        
    con.commit()
    
    row = cur.fetchone()
    print row[0], row[1]
con.close()
