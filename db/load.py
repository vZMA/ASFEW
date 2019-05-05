import sqlite3

def main():
    cn = sqlite3.connect('sector.db')
    c = cn.cursor()

    # Load tables with data required from user

    #fix/range used to pull automatic data from web (e.g. 1000 nm from PHK)
    c.execute("DELETE FROM config")
    c.execute("""INSERT INTO config VALUES (
                    'PHK', 1000 
                )""")

    #defines colors for VRC, add as many as neded for your sector file
    c.execute("DELETE FROM colors")
    c.execute("""INSERT INTO colors (ColorName, ColorVal)
                VALUES
                ('Teal', 8421376), 
                ('Coast', 13056),
                ('Tracon', 3815994),
                ('CENTER', 13408665),
                ('LOWCTR', 3815994),
                ('Protect', 11010048),
                ('MOA', 556500),
                ('Prohibit', 1000),
                ('Restrict', 1200),
                ('Runway', 16777215),
                ('Taxiway', 16711680),
                ('Building', 4605520),
                ('Tower', 16711935),
                ('Select', 8421504),
                ('Parking', 32768),
                ('Expand', 16711680),
                ('Stopline', 255),
                ('ramp', 32768),
                ('RampControl', 7895040),
                ('ClassB', 6697728),
                ('ClassC', 32896),
                ('ClassD', 4194368),
                ('ModeC', 7895040),
                ('ATA', 16712064),
                ('DTA', 8388992),
                ('AG', 8421504),
                ('CTR', 556500),
                ('IAF', 8421504),
                ('MYNNW', 128),
                ('VMBG', 3815994),
                ('VMFG', 65793),
                ('TXWM', 10772514),
                ('RWM', 6697779),
                ('NEW', 556500),
                ('NBuilding', 556500),
                ('ZMA', 8358280),
                ('APCHBDRYS', 4280401),
                ('JET', 2959146),
                ('QY', 2959146),
                ('STAR', 4012111),
                ('MIT', 8358280)
              """)

    #values used to build sector file [INFO] section
    c.execute("DELETE FROM info")
    c.execute("""INSERT INTO info VALUES (
                'ZMA/ZMO Sector File (1813)', --sector file name
                'MIA_CTR', --default position
                'KMIA', --default airport
                'N026.50.12.787', --default center lat
                'W080.51.16.679', --default center lon
                '60.000', --nm per degree lat
                '54.000', --nm per degree lon
                '5.480', --magnetic variation
                '1.000' --sector scale value
                )""")

    #manual VORs that won't be pulled from other data sources
    c.execute("DELETE FROM vor WHERE type = 'MANUAL'")
    c.execute("""INSERT INTO vor (ident, frequency, lat, lon, comment, type)
                VALUES
                ('ZFP','113.20','N026.33.19.250','W078.41.52.250','FREEPORT','MANUAL'),
                ('UHA','116.10','N022.58.43.820','W082.25.35.930','HABANA CUBA','MANUAL')
               """)

    #manual NDBs that won't be pulled from other data sources
    c.execute("DELETE FROM ndb WHERE type = 'MANUAL'")
    c.execute("""INSERT INTO ndb (ident, frequency, lat, lon, comment, type)
                VALUES
                ('CZM','201','N020.31.25.000','W086.55.54.000','COZUMEL','MANUAL'),
                ('CBC','415','N019.41.23.910','W079.51.24.380','CAYMAN BRAC','MANUAL')
               """)

    #manual NDBs that won't be pulled from other data sources
    c.execute("DELETE FROM airport WHERE type = 'MANUAL'")
    c.execute("""INSERT INTO airport (grouptitle, ident, frequency, lat, lon, airspace, comment, type)
                VALUES
                ('CUBA','MUBA', '000.000', 'N020.21.55.000','W074.30.22.000','','','MANUAL'),
                ('CUBA','MUBY', '000.000', 'N020.23.47.000','W076.37.17.000','','','MANUAL')
               """)

    #manual runways that won't be pulled from other data sources
    c.execute("DELETE FROM runway WHERE type = 'MANUAL'")
    c.execute("""INSERT INTO runway (airport, end1, mag1, end2, mag2, lat1, lon1, lat2, lon2, comment, type)
                VALUES
                ('KUNK','30','000','12','000','N031.08.10.999','W085.02.21.000','N031.08.40.999','W085.03.14.998','','MANUAL')
               """)
    
    cn.commit()
    cn.close()

if __name__=="__main__":
    main()
