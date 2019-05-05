import sqlite3
import urllib

def main():
    cn = sqlite3.connect('../db/sector.db')
    c = cn.cursor()

    #get file from myfsim
    dataFile = urllib.URLopener()
    dataFile.retrieve("http://www.myfsim.com/sectorfilecreation/Result.php?BASE=PHK&DIST=100&NOPTS=1", "data/myfsim.dat")

            
    cn.close()

if __name__=="__main__":
    main()
