import sqlite3

def main():
    cn = sqlite3.connect('../db/sector.db')
    c = cn.cursor()

    
    c.execute("DELETE FROM vor WHERE type = 'AUTO'")
    f = open("data/vor.dat", "r")
    for x in f:
        if x[:1] != ";":
            t = x.split()
            c.execute("""INSERT INTO vor (ident, frequency, lat, lon, comment, type)
            VALUES ('%s','%s','%s','%s','%s','AUTO')
           """ % (t[0], t[1], t[2], t[3], t[4]))

    c.execute("DELETE FROM ndb WHERE type = 'AUTO'")
    f = open("data/ndb.dat", "r")
    for x in f:
        if x[:1] != ";":
            t = x.split()
            c.execute("""INSERT INTO ndb (ident, frequency, lat, lon, comment, type)
            VALUES ('%s','%s','%s','%s','%s','AUTO')
           """ % (t[0], t[1], t[2], t[3], t[4]))

    c.execute("DELETE FROM airport WHERE type = 'AUTO'")
    f = open("data/apt.dat", "r")
    for x in f:
        if x[:1] != ";":
            t = x.split()
            c.execute("""INSERT INTO airport (grouptitle, ident, frequency, lat, lon, airspace, comment, type)
            VALUES ('','%s','%s','%s','%s','','','AUTO')
           """ % (t[0], t[1], t[2], t[3]))

    c.execute("DELETE FROM fixes WHERE type = 'AUTO'")
    f = open("data/int.dat", "r")
    for x in f:
        if x[:1] != ";":
            t = x.split()
            c.execute("""INSERT INTO fixes (name, lat, lon, comment, type)
            VALUES ('%s','%s','%s','','AUTO')
           """ % (t[0], t[1], t[2]))

    c.execute("DELETE FROM airwaylow WHERE type = 'AUTO'")
    f = open("data/airwaylow.dat", "r")
    for x in f:
        if x[:1] != ";" and x[:1] != "[":
            t = x.split()
            c.execute("""INSERT INTO airwaylow (name, lat1, lon1, lat2, lon2, comment, type)
            VALUES ('%s','%s','%s','%s','%s','','AUTO')
           """ % (t[0], t[1], t[2], t[3], t[4]))

    c.execute("DELETE FROM airwayhigh WHERE type = 'AUTO'")
    f = open("data/airwayhigh.dat", "r")
    for x in f:
        if x[:1] != ";" and x[:1] != "[":
            t = x.split()
            c.execute("""INSERT INTO airwayhigh (name, lat1, lon1, lat2, lon2, comment, type)
            VALUES ('%s','%s','%s','%s','%s','','AUTO')
           """ % (t[0], t[1], t[2], t[3], t[4]))            

    cn.commit()
    cn.close()

if __name__=="__main__":
    main()
