import sqlite3
import datetime

def psep(lines, w):
    n = 0
    while n < lines:
        n += 1
        w.write('\n')

def writeit(content, w):
    w.write(content + '\n')

def main():
    cn = sqlite3.connect('../db/sector.db')
    c = cn.cursor()
    f = open("data/sector.sct2", "w")

    #get [INFO] from database
    #some of it is needed to write headers
    c.execute("SELECT * FROM info")
    info = c.fetchone()

    #load colors
    c.execute("SELECT * FROM colors")
    colors = c.fetchall()
    
    #write file
    writeit(";This sector file produced by ASFEW (Automated Sector File Editing Workflow)", f)
    writeit(";https://github.com/vZMA/ASFEW", f)
    writeit(";Created " + str(datetime.datetime.now()), f)

    psep(1,f)

    for color in colors:
        writeit('#define ' + color[0] + ' ' + str(color[1]), f)

    psep(1,f)

    #[INFO]
    writeit("[INFO]", f)
    writeit(info[0], f)
    writeit(info[1], f)
    writeit(info[2], f)
    writeit(info[3], f)
    writeit(info[4], f)
    writeit(info[5], f)
    writeit(info[6], f)
    writeit(info[7], f)
    writeit(info[8], f)

    psep(1,f)

    #[VOR]
    writeit("[VOR]", f)
    c.execute("SELECT * FROM vor order by ident")
    vors = c.fetchall()

    for vor in vors:
        writeit(vor[0] + ' ' + vor[1] + ' ' + vor[2] + ' ' + vor[3], f)

    psep(1,f)

    #[NDB]
    writeit("[NDB]", f)
    c.execute("SELECT * FROM ndb order by ident")
    ndbs = c.fetchall()

    for ndb in ndbs:
        writeit(ndb[0].ljust(3) + ' ' + ndb[1].ljust(6) + ' ' + ndb[2] + ' ' + ndb[3], f)

    psep(1,f)

    #[AIRPORT]
    writeit("[AIRPORT]", f)
    c.execute("SELECT * FROM airport order by ident")
    apts = c.fetchall()

    for apt in apts:
        writeit(apt[1].ljust(4) + ' ' + apt[2] + ' ' + apt[3] + ' ' + apt[4], f)

    psep(1,f)

    #[RUNWAY]
    writeit("[RUNWAY]", f)
    c.execute("SELECT * FROM runway order by airport, end1")
    rwys = c.fetchall()

    for rwy in rwys:
        writeit(rwy[1] + ' ' + rwy[3] + ' ' + rwy[2] + ' ' + rwy[4] + ' ' + rwy[5] + ' ' + rwy[6] + ' ' + rwy[7] + ' ' + rwy[8], f)

    psep(1,f)

    #[FIXES]
    writeit("[FIXES]", f)
    c.execute("SELECT * FROM fixes order by name")
    fixes = c.fetchall()

    for fix in fixes:
        writeit(fix[0] + ' ' + fix[1] + ' ' + fix[2], f)

    psep(1,f)

    #[ARTCC]
    writeit("[ARTCC]", f)
    psep(1,f)
    
    #[ARTCC HIGH]
    writeit("[ARTCC HIGH]", f)
    psep(1,f)
    
    #[ARTCC LOW]
    writeit("[ARTCC LOW]", f)
    psep(1,f)
    
    #[SID]
    writeit("[SID]", f)
    psep(1,f)
    
    #[STAR]
    writeit("[STAR]", f)
    psep(1,f)
    
    #[LOW AIRWAY]
    writeit("[LOW AIRWAY]", f)
    psep(1,f)
    
    #[HIGH AIRWAY]
    writeit("[HIGH AIRWAY]", f)
    psep(1,f)
    
    #[GEO]
    writeit("[GEO]", f)
    psep(1,f)
    
    #[LABELS]
    writeit("[LABELS]", f)
    psep(1,f)
    
    cn.close()

if __name__=="__main__":
    main()
