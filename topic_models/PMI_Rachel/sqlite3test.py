import sqlite3
from datetime import datetime as dt

if __name__=="__main__":
    conn = sqlite3.connect('5gms_db.db')
    c = conn.cursor()
    w1 = raw_input("word 1:")
    w2 = raw_input("word 2:")
    
    for row in c.execute(q):
            print row
        print "End:",dt.now()
        q = raw_input("Query")
        print "Started:",dt.now()

