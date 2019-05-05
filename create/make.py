import sqlite3

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
    writeit(";Created XXXXXXXXXXXX", f)

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

    psep(15,f)

    #[VOR]
    

    
    cn.close()

if __name__=="__main__":
    main()
