import sqlite3

if __name__=='__main__':
    conn = sqlite3.connect('5gms_db_idx.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS five_grams''')
    c.execute('''CREATE TABLE five_grams (id1 INT,id2 INT, id3 INT, id4 INT, id5 INT, freq INT)''')
# indices
    c.execute("CREATE INDEX id1_2 on five_grams (id1,id2)")
    c.execute("CREATE INDEX id1_3 on five_grams (id1,id3)")
    c.execute("CREATE INDEX id1_4 on five_grams (id1,id4)")
    c.execute("CREATE INDEX id1_5 on five_grams (id1,id5)")
    c.execute("CREATE INDEX id2_3 on five_grams (id2,id3)")
    c.execute("CREATE INDEX id2_4 on five_grams (id2,id4)")
    c.execute("CREATE INDEX id2_5 on five_grams (id2,id5)")
    c.execute("CREATE INDEX id3_1 on five_grams (id3,id4)")
    c.execute("CREATE INDEX id3_2 on five_grams (id3,id5)")
    c.execute("CREATE INDEX id4_5 on five_grams (id4,id5)")
    c.execute("PRAGMA synchronous=OFF")
    c.execute("PRAGMA journal_mode=OFF")
#    c.execute("PRAGMA cache_size=4000")
#    conn.commit()
    conn.close()
