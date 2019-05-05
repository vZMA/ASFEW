import sqlite3

def main():
    cn = sqlite3.connect('sector.db')
    c = cn.cursor()

    # Define tables for future use in database
    
    c.execute("""CREATE TABLE config (
                    CenterFix text,
                    CenterRange integer
                )""")

    c.execute("""CREATE TABLE colors (
                    ColorName text,
                    ColorVal integer
                )""")

    c.execute("""CREATE TABLE info (
                    SectorFileName text,
                    DefaultCallsign text,
                    DefaultAirport text,
                    DefaultCenterLat text,
                    DefaultCenterLon text,
                    MilesPerDegreeLat text,
                    MilesPerDesgreeLon text,
                    MagneticVariation text,
                    SectorScale text
                )""")

    c.execute("""CREATE TABLE vor (
                    ident text,
                    frequency text,
                    lat text,
                    lon text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE ndb (
                    ident text,
                    frequency text,
                    lat text,
                    lon text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE airport (
                    grouptitle text,
                    ident text,
                    frequency text,
                    lat text,
                    lon text,
                    airspace text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE runway (
                    airport text,
                    end1 text,
                    mag1 text,
                    end2 text,
                    mag2 text,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,                    
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE fixes (
                    name text,
                    lat text,
                    lon text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE high (
                    name text,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,                    
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE low (
                    name text,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,                    
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE artcc (
                    name text,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,                    
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE geo (
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,                    
                    color text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE labels (
                    grouptitle text,
                    name text,
                    lat text,
                    lon text,
                    color text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE sid (
                    name text,
                    sequence integer,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,
                    color text,
                    comment text,
                    type text
                )""")

    c.execute("""CREATE TABLE star (
                    name text,
                    sequence integer,
                    lat1 text,
                    lon1 text,
                    lat2 text,
                    lon2 text,
                    color text,
                    comment text,
                    type text
                )""")
        
    cn.commit()
    cn.close()

if __name__=="__main__":
    main()
